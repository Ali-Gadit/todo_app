"""Custom exception types for Todo Console App."""

class TaskNotFound(Exception):
    """Raised when task ID does not exist in task list."""
    pass


class InvalidTitle(Exception):
    """Raised when task title is empty or exceeds length limit."""
    pass
