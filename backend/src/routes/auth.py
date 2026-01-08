"""
Authentication routes for user login, registration, and session management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext

from ..auth import create_access_token, get_current_user
from ..db import get_session
from ..models import User
from ..schemas.auth import TokenResponse, UserCreate, UserLogin, UserResponse

router = APIRouter(tags=["Authentication"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_data: UserCreate, session = Depends(get_session)) -> TokenResponse:
    """Register a new user and return a JWT token."""
    from sqlalchemy import select

    # Check if email exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_email = result.scalar_one_or_none()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if username exists
    result = await session.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_username = result.scalar_one_or_none()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate JWT token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        username=user.username,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, session = Depends(get_session)) -> TokenResponse:
    """Authenticate a user and return a JWT token."""
    from sqlalchemy import select

    result = await session.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate JWT token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        username=user.username,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post("/logout")
async def logout() -> dict:
    """Logout the current user."""
    # JWT tokens are stateless, so we just inform the client to remove it
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get the current authenticated user's information."""
    return UserResponse.model_validate(current_user)
