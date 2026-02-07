from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Text, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """Message model for chat turns."""

    id: str = Field(primary_key=True) # Use string ID for ChatKit compatibility
    conversation_id: str = Field(foreign_key="conversation.id", ondelete="CASCADE", index=True)
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE", index=True)
    role: str = Field(max_length=50) # "user" or "assistant"
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow),
    )

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship()

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, role={self.role})>"