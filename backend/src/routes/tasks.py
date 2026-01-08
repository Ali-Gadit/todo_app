"""
Task routes for CRUD operations on todo items.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select

from ..auth import get_current_user
from ..db import get_session
from ..models import Task, User
from ..schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(tags=["Tasks"])


@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session = Depends(get_session),
) -> List[TaskResponse]:
    """
    Get all tasks for the current user.
    Supports filtering by status, priority, and search query.
    """
    async with session:
        # Build base query
        query = select(Task).where(Task.user_id == current_user.id)

        # Apply status filter
        if status_filter:
            query = query.where(Task.status == status_filter)

        # Apply priority filter
        if priority:
            query = query.where(Task.priority == priority)

        # Apply search filter (title or description)
        if search:
            search_term = f"%{search}%"
            query = query.where(
                (Task.title.ilike(search_term)) |
                (Task.description.ilike(search_term))
            )

        # Order by created_at descending (newest first)
        query = query.order_by(Task.created_at.desc())

        result = await session.execute(query)
        tasks = result.scalars().all()
        return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session = Depends(get_session),
) -> TaskResponse:
    """Get a specific task by ID."""
    async with session:
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return TaskResponse.model_validate(task)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session = Depends(get_session),
) -> TaskResponse:
    """Create a new task."""
    async with session:
        task = Task(**task_data.model_dump(), user_id=current_user.id)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session = Depends(get_session),
) -> TaskResponse:
    """Update an existing task."""
    async with session:
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await session.commit()
        await session.refresh(task)
        return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session = Depends(get_session),
) -> None:
    """Delete a task."""
    async with session:
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        await session.delete(task)
        await session.commit()


@router.get("/stats/summary")
async def get_task_stats(
    current_user: User = Depends(get_current_user),
    session = Depends(get_session),
) -> dict:
    """Get task statistics for the current user."""
    async with session:
        # Count by status
        result = await session.execute(
            select(Task.status, func.count(Task.id))
            .where(Task.user_id == current_user.id)
            .group_by(Task.status)
        )
        status_counts = dict(result.all())

        # Total count
        result = await session.execute(
            select(func.count(Task.id)).where(Task.user_id == current_user.id)
        )
        total = result.scalar()

        return {
            "total": total,
            "by_status": status_counts,
            "pending": status_counts.get("pending", 0),
            "in_progress": status_counts.get("in_progress", 0),
            "completed": status_counts.get("completed", 0),
        }
