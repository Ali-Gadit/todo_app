"""
JWT authentication module for token generation and verification.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from .config import settings


class TokenPayload(BaseModel):
    """JWT token payload schema."""
    sub: int  # User ID
    email: str
    username: str
    exp: datetime


class CurrentUser(BaseModel):
    """Current authenticated user."""
    id: int
    email: str
    username: str


# HTTP Bearer token security scheme
security = HTTPBearer()


def create_access_token(
    user_id: int,
    email: str,
    username: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: The user's ID
        email: The user's email
        username: The user's username
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # Default 7 days

    to_encode = {
        "sub": str(user_id),
        "email": email,
        "username": username,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def verify_token(token: str) -> TokenPayload:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token to verify

    Returns:
        TokenPayload with decoded claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token_data = TokenPayload(**payload)
        return token_data
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    """
    FastAPI dependency to get the current authenticated user.

    Args:
        credentials: HTTP Bearer credentials from request header

    Returns:
        CurrentUser with user information

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    token_data = verify_token(token)

    return CurrentUser(
        id=int(token_data.sub),
        email=token_data.email,
        username=token_data.username,
    )


def decode_token_without_verification(token: str) -> Optional[dict]:
    """
    Decode a token without verification (for debugging/logging).

    Args:
        token: The JWT token to decode

    Returns:
        Decoded payload or None if invalid
    """
    try:
        return jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
    except JWTError:
        return None
