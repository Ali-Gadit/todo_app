"""
Task schemas for the Todo application.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..models import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    """Base task schema with common fields."""

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Task creation schema."""

    pass


class TaskUpdate(BaseModel):
    """Task update schema."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Task response schema."""

    id: int
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
