"""TaskService for Todo Console App.

Provides CRUD (Create, Read, Update, Delete) operations
and status management for tasks in memory.
"""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional
from todo_app.models.task import Task
from todo_app.lib.exceptions import TaskNotFound, InvalidTitle


class TaskService:
    """Manages task storage and CRUD operations with file persistence."""

    MAX_TITLE_LENGTH: int = 1000
    MAX_DESCRIPTION_LENGTH: int = 1000
    DEFAULT_STORAGE_FILE: str = "tasks.json"

    def __init__(self, storage_path: Optional[str] = None) -> None:
        """Initialize task service.

        Args:
            storage_path: Path to JSON storage file. Defaults to 'tasks.json' in project root.
        """
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            # Default to root of the project
            self.storage_path = Path(__file__).parent.parent.parent / self.DEFAULT_STORAGE_FILE

        self._tasks: list[Task] = []
        self._next_id: int = 1
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from the JSON storage file."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._tasks = [Task(**task_data) for task_data in data]
                if self._tasks:
                    self._next_id = max(task.id for task in self._tasks) + 1
        except (json.JSONDecodeError, IOError):
            # If file is corrupt or unreadable, start with empty list
            self._tasks = []
            self._next_id = 1

    def _save_tasks(self) -> None:
        """Save tasks to the JSON storage file."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([asdict(task) for task in self._tasks], f, indent=4)
        except IOError:
            # In a production app, we'd handle this more gracefully
            pass

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the task list."""
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
        self._save_tasks()
        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound(f"Task with ID {task_id} not found")

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks in the task list."""
        return list(self._tasks)

    def update_task(self, task_id: int, title: str, description: Optional[str] = None) -> Task:
        """Update an existing task's title and/or description."""
        task = self.get_task(task_id)
        self._validate_title(title)

        task.title = title
        if description is not None:
            self._validate_description(description)
            task.description = description

        self._save_tasks()
        return task

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        task.completed = True
        self._save_tasks()
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete."""
        task = self.get_task(task_id)
        task.completed = False
        self._save_tasks()
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task from the task list."""
        task = self.get_task(task_id)
        self._tasks.remove(task)
        self._save_tasks()

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
