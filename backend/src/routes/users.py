"""
User routes for user-related operations.
"""

from fastapi import APIRouter, Depends

from ..auth import get_current_user
from ..models import User
from ..schemas import UserResponse

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get the current authenticated user."""
    return UserResponse.model_validate(current_user)
