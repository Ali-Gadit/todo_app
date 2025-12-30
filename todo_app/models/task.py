"""Task entity dataclass for Todo Console App."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential numeric identifier (starting from 1)
        title: Required task title/name (non-empty, max 1000 chars)
        description: Optional task details (max 1000 chars, defaults to empty string)
        completed: Task completion status (True/False, defaults to False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
