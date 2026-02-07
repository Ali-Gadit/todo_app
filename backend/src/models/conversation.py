from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""

    id: str = Field(primary_key=True) # Use string ID for ChatKit compatibility
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow),
    )

    # Relationships
    user: Optional["User"] = Relationship()
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"