"""TaskService for Todo Console App.

Provides CRUD (Create, Read, Update, Delete) operations
and status management for tasks in memory.
"""

from typing import Optional
from todo_app.models.task import Task
from todo_app.lib.exceptions import TaskNotFound, InvalidTitle


class TaskService:
    """Manages in-memory task storage and CRUD operations."""

    MAX_TITLE_LENGTH: int = 1000
    MAX_DESCRIPTION_LENGTH: int = 1000

    def __init__(self) -> None:
        """Initialize task service with empty task list and ID counter."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the task list.

        Args:
            title: Task title (required, non-empty, <=1000 chars)
            description: Optional task description (<=1000 chars)

        Returns:
            New task object with assigned sequential ID

        Raises:
            InvalidTitle: If title is empty or exceeds length limit
        """
        self._validate_title(title)
        self._validate_description(description)

        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task object matching provided ID

        Raises:
            TaskNotFound: If task_id does not exist in task list
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound(f"Task with ID {task_id} not found")

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks in the task list.

        Returns:
            All tasks in creation order (by ID)
        """
        return list(self._tasks)

    def update_task(self, task_id: int, title: str, description: Optional[str] = None) -> Task:
        """Update an existing task's title and/or description.

        Args:
            task_id: Task ID to update
            title: New task title (required, non-empty, <=1000 chars)
            description: New task description (optional, <=1000 chars). If None, keeps existing

        Returns:
            Updated task object with new title/description

        Raises:
            TaskNotFound: If task_id does not exist
            InvalidTitle: If title is empty or exceeds length limit
        """
        task = self.get_task(task_id)
        self._validate_title(title)

        task.title = title
        if description is not None:
            self._validate_description(description)
            task.description = description
        return task

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as completed.

        Args:
            task_id: Task ID to mark complete

        Returns:
            Updated task with completed=True

        Raises:
            TaskNotFound: If task_id does not exist
        """
        task = self.get_task(task_id)
        task.completed = True
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: Task ID to mark incomplete

        Returns:
            Updated task with completed=False

        Raises:
            TaskNotFound: If task_id does not exist
        """
        task = self.get_task(task_id)
        task.completed = False
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task from the task list.

        Args:
            task_id: Task ID to delete

        Raises:
            TaskNotFound: If task_id does not exist

        Note:
            Deleting a task does not renumber remaining task IDs.
        """
        task = self.get_task(task_id)
        self._tasks.remove(task)

    def _validate_title(self, title: str) -> None:
        """Validate task title.

        Args:
            title: Title to validate

        Raises:
            InvalidTitle: If title is empty or exceeds length limit
        """
        if not title or not title.strip():
            raise InvalidTitle("Task title cannot be empty")
        if len(title) > self.MAX_TITLE_LENGTH:
            raise InvalidTitle(f"Task title exceeds maximum length ({self.MAX_TITLE_LENGTH} characters)")

    def _validate_description(self, description: str) -> None:
        """Validate task description.

        Args:
            description: Description to validate

        Raises:
            InvalidTitle: If description exceeds length limit
        """
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise InvalidTitle(f"Task description exceeds maximum length ({self.MAX_DESCRIPTION_LENGTH} characters)")
