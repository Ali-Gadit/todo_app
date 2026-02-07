import json
from agents import function_tool, RunContextWrapper
from chatkit.agents import AgentContext
from typing import Optional, List, Any, Dict
from sqlmodel import select
from ..db import async_session_factory
from ..models.task import Task, TaskStatus

# Helper to get a session (since tools are async functions)
async def get_db_session():
    return async_session_factory()

async def add_task_impl(user_id: str, title: str, description: str = "") -> str:
    """Core logic for adding a task."""
    print(f"DEBUG: add_task_impl user_id={user_id}, title='{title}'")
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return json.dumps({"status": "error", "message": f"Invalid user_id format: {user_id}"})

    async with async_session_factory() as session:
        new_task = Task(user_id=user_id_int, title=title, description=description)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        print(f"DEBUG: add_task_impl success: task_id={new_task.id}")
        
        return json.dumps({
            "task_id": new_task.id,
            "status": "created",
            "title": new_task.title
        })

@function_tool
async def add_task(ctx: RunContextWrapper[AgentContext], title: str, description: Optional[str] = None) -> str:
    """
    Create a new task for the user.

    Args:
        title: The title of the task.
        description: Optional detailed description of the task.
    """
    user_id = ctx.context.request_context.get("user_id")
    return await add_task_impl(user_id, title, description or "")

async def list_tasks_impl(user_id: str, status: str = "all") -> str:
    """Core logic for listing tasks."""
    print(f"DEBUG: list_tasks_impl user_id={user_id}, status='{status}'")
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return json.dumps([{"error": f"Invalid user_id: {user_id}"}])

    async with async_session_factory() as session:
        query = select(Task).where(Task.user_id == user_id_int)
        
        if status == "pending":
            query = query.where(Task.status == TaskStatus.PENDING)
        elif status == "completed":
            query = query.where(Task.status == TaskStatus.COMPLETED)
        
        result = await session.execute(query)
        tasks = result.scalars().all()
        print(f"DEBUG: list_tasks_impl found {len(tasks)} tasks")
        
        return json.dumps([
            {
                "id": t.id,
                "title": t.title,
                "completed": t.status == TaskStatus.COMPLETED
            }
            for t in tasks
        ])

@function_tool
async def list_tasks(ctx: RunContextWrapper[AgentContext], status: Optional[str] = None) -> str:
    """
    Retrieve tasks from the list, optionally filtered by status.

    Args:
        status: Filter tasks by status. One of 'all', 'pending', or 'completed'.
    """
    user_id = ctx.context.request_context.get("user_id")
    return await list_tasks_impl(user_id, status or "all")

async def complete_task_impl(user_id: str, task_id: int) -> str:
    """Core logic for completing a task."""
    print(f"DEBUG: complete_task_impl user_id={user_id}, task_id={task_id}")
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return json.dumps({"status": "error", "message": "Invalid user_id"})

    async with async_session_factory() as session:
        task = await session.get(Task, task_id)
        if not task:
            print(f"DEBUG: complete_task_impl task not found: {task_id}")
            return json.dumps({"status": "error", "message": "Task not found"})
            
        if task.user_id != user_id_int:
             print(f"DEBUG: complete_task_impl user mismatch: {task.user_id} != {user_id_int}")
             return json.dumps({"status": "error", "message": "Task not found"})

        task.status = TaskStatus.COMPLETED
        session.add(task)
        await session.commit()
        await session.refresh(task)
        print(f"DEBUG: complete_task_impl success: {task_id}")
        
        return json.dumps({
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        })

@function_tool
async def complete_task(ctx: RunContextWrapper[AgentContext], task_id: int) -> str:
    """
    Mark a task as complete.

    Args:
        task_id: The ID of the task to mark as complete.
    """
    user_id = ctx.context.request_context.get("user_id")
    return await complete_task_impl(user_id, task_id)

async def delete_task_impl(user_id: str, task_id: int) -> str:
    """Core logic for deleting a task."""
    print(f"DEBUG: delete_task_impl called with user_id={user_id}, task_id={task_id}")
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        print(f"DEBUG: delete_task_impl invalid user_id: {user_id}")
        return json.dumps({"status": "error", "message": "Invalid user_id"})

    async with async_session_factory() as session:
        task = await session.get(Task, task_id)
        if not task:
            print(f"DEBUG: delete_task_impl task not found: {task_id}")
            return json.dumps({"status": "error", "message": "Task not found"})
            
        if task.user_id != user_id_int:
             print(f"DEBUG: delete_task_impl user mismatch: task.user_id={task.user_id}, user_id_int={user_id_int}")
             return json.dumps({"status": "error", "message": "Task not found"})

        task_title = task.title
        await session.delete(task)
        await session.commit()
        print(f"DEBUG: delete_task_impl success: {task_id}")
        
        return json.dumps({
            "task_id": task_id,
            "status": "deleted",
            "title": task_title
        })

@function_tool
async def delete_task(ctx: RunContextWrapper[AgentContext], task_id: int) -> str:
    """
    Remove a task from the list.

    Args:
        task_id: The ID of the task to delete.
    """
    user_id = ctx.context.request_context.get("user_id")
    return await delete_task_impl(user_id, task_id)

async def update_task_impl(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
    """Core logic for updating a task."""
    print(f"DEBUG: update_task_impl user_id={user_id}, task_id={task_id}")
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return json.dumps({"status": "error", "message": "Invalid user_id"})

    async with async_session_factory() as session:
        task = await session.get(Task, task_id)
        if not task:
            print(f"DEBUG: update_task_impl task not found: {task_id}")
            return json.dumps({"status": "error", "message": "Task not found"})
            
        if task.user_id != user_id_int:
             print(f"DEBUG: update_task_impl user mismatch: {task.user_id} != {user_id_int}")
             return json.dumps({"status": "error", "message": "Task not found"})

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
            
        session.add(task)
        await session.commit()
        await session.refresh(task)
        print(f"DEBUG: update_task_impl success: {task_id}")
        
        return json.dumps({
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        })

@function_tool
async def update_task(ctx: RunContextWrapper[AgentContext], task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
    """
    Modify task title or description.

    Args:
        task_id: The ID of the task to update.
        title: New title for the task (optional).
        description: New description for the task (optional).
    """
    user_id = ctx.context.request_context.get("user_id")
    return await update_task_impl(user_id, task_id, title, description)