# Service Interface Contract: Task Service

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Purpose**: Define TaskService method signatures and contracts

## Overview

TaskService provides CRUD (Create, Read, Update, Delete) operations and status management for tasks in memory. All methods raise domain-specific exceptions for error handling.

---

## Method Contracts

### add_task

Add a new task to the task list.

**Signature**:
```python
def add_task(title: str, description: str = "") -> Task
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| title | str | Yes | Non-empty, <=1000 chars |
| description | str | No | Optional, <=1000 chars |

**Returns**:
- Type: `Task`
- New task object with assigned sequential ID, provided title, description, and completed=False

**Raises**:
| Exception | Condition |
|-----------|-----------|
| InvalidTitle | If title is empty or exceeds 1000 chars |

**Example**:
```python
task = task_service.add_task("Buy groceries", "Weekly shopping")
# Returns: Task(id=1, title="Buy groceries", description="Weekly shopping", completed=False)
```

---

### get_task

Retrieve a task by ID.

**Signature**:
```python
def get_task(task_id: int) -> Task
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| task_id | int | Yes | Positive integer |

**Returns**:
- Type: `Task`
- Task object matching provided ID

**Raises**:
| Exception | Condition |
|-----------|-----------|
| TaskNotFound | If task_id does not exist in task list |

**Example**:
```python
task = task_service.get_task(1)
# Returns: Task(id=1, title="Buy groceries", description="Weekly shopping", completed=False)

task = task_service.get_task(999)
# Raises: TaskNotFound("Task with ID 999 not found")
```

---

### list_tasks

Retrieve all tasks in the task list.

**Signature**:
```python
def list_tasks() -> list[Task]
```

**Parameters**: None

**Returns**:
- Type: `list[Task]`
- All tasks in creation order (by ID)

**Raises**: None

**Example**:
```python
tasks = task_service.list_tasks()
# Returns: [
#     Task(id=1, title="Buy groceries", description="Weekly shopping", completed=False),
#     Task(id=2, title="Complete project", description="", completed=True),
# ]
```

---

### update_task

Update an existing task's title and/or description.

**Signature**:
```python
def update_task(task_id: int, title: str, description: str = None) -> Task
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| task_id | int | Yes | Positive integer, task must exist |
| title | str | Yes | Non-empty, <=1000 chars |
| description | str | No | Optional, <=1000 chars. If None, keep existing |

**Returns**:
- Type: `Task`
- Updated task object with new title/description

**Raises**:
| Exception | Condition |
|-----------|-----------|
| TaskNotFound | If task_id does not exist |
| InvalidTitle | If title is empty or exceeds 1000 chars |

**Example**:
```python
task = task_service.update_task(1, "Buy groceries 🛒")
# Updates title only, keeps existing description

task = task_service.update_task(1, "Buy groceries 🛒", "Weekly shopping list")
# Updates both title and description
```

---

### mark_complete

Mark a task as completed.

**Signature**:
```python
def mark_complete(task_id: int) -> Task
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| task_id | int | Yes | Positive integer, task must exist |

**Returns**:
- Type: `Task`
- Updated task with completed=True

**Raises**:
| Exception | Condition |
|-----------|-----------|
| TaskNotFound | If task_id does not exist |

**Example**:
```python
task = task_service.mark_complete(1)
# Returns: Task(id=1, title="Buy groceries", description="Weekly shopping", completed=True)
```

---

### mark_incomplete

Mark a task as incomplete.

**Signature**:
```python
def mark_incomplete(task_id: int) -> Task
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| task_id | int | Yes | Positive integer, task must exist |

**Returns**:
- Type: `Task`
- Updated task with completed=False

**Raises**:
| Exception | Condition |
|-----------|-----------|
| TaskNotFound | If task_id does not exist |

**Example**:
```python
task = task_service.mark_incomplete(1)
# Returns: Task(id=1, title="Buy groceries", description="Weekly shopping", completed=False)
```

---

### delete_task

Delete a task from the task list.

**Signature**:
```python
def delete_task(task_id: int) -> None
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| task_id | int | Yes | Positive integer, task must exist |

**Returns**: None

**Raises**:
| Exception | Condition |
|-----------|-----------|
| TaskNotFound | If task_id does not exist |

**Note**: Deleting a task does not renumber remaining task IDs.

**Example**:
```python
task_service.delete_task(1)
# Task removed from list, remaining task IDs unchanged
```

---

## Type Definitions

### Task

```python
@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

---

## Exception Types

### TaskNotFound

Raised when a task with the specified ID does not exist.

**Signature**:
```python
class TaskNotFound(Exception):
    """Raised when task ID does not exist in task list."""
    pass
```

**Usage**:
```python
try:
    task = task_service.get_task(999)
except TaskNotFound:
    print("Error: Task with ID 999 not found")
```

---

### InvalidTitle

Raised when task title is empty or exceeds length limit.

**Signature**:
```python
class InvalidTitle(Exception):
    """Raised when task title is empty or exceeds length limit."""
    pass
```

**Usage**:
```python
try:
    task = task_service.add_task("")
except InvalidTitle:
    print("Error: Task title cannot be empty")
```

---

## Invariants

### Service-Level Invariants

| Invariant | Rule | Enforcement Method |
|-----------|------|-------------------|
| S-001 | Task IDs are sequential, starting from 1 | Internal counter, auto-increment |
| S-002 | Task IDs are unique on creation | Counter ensures uniqueness |
| S-003 | Task IDs are stable on delete | Delete does not renumber remaining tasks |
| S-004 | All task titles are non-empty | add_task() and update_task() validation |
| S-005 | All task fields respect length limits (1000 chars) | add_task() and update_task() validation |
| S-006 | completed status is always boolean | Task dataclass type enforcement |

---

## State Management

### Internal State

```python
class TaskService:
    def __init__(self) -> None:
        """Initialize task service with empty task list and ID counter."""
        self._tasks: list[Task] = []
        self._next_id: int = 1
```

**State Variables**:
- `_tasks: list[Task]` - In-memory task storage
- `_next_id: int` - Sequential ID counter

**Note**: Internal state is private (prefixed with `_`) to enforce encapsulation.

---

## Usage Examples

### Complete Task Lifecycle

```python
# Initialize service
task_service = TaskService()

# Add tasks
task1 = task_service.add_task("Buy groceries", "Weekly shopping")
task2 = task_service.add_task("Complete project")

# List all tasks
tasks = task_service.list_tasks()
# Returns: [Task(id=1, ...), Task(id=2, ...)]

# Update task
task1 = task_service.update_task(1, "Buy groceries 🛒")

# Mark complete
task2 = task_service.mark_complete(2)

# Delete task
task_service.delete_task(1)

# Final list
tasks = task_service.list_tasks()
# Returns: [Task(id=2, ...)] - Note: ID is 2, not 1 (stable IDs)
```

### Error Handling

```python
try:
    task = task_service.get_task(999)
except TaskNotFound as e:
    print(f"Error: {e}")
    # Output: Error: Task with ID 999 not found

try:
    task = task_service.add_task("")
except InvalidTitle as e:
    print(f"Error: {e}")
    # Output: Error: Task title cannot be empty
```

---

## Summary

Service interface defines:
- 7 methods (add_task, get_task, list_tasks, update_task, mark_complete, mark_incomplete, delete_task)
- Complete parameter and return type annotations
- Exception contracts for 2 custom exception types
- 6 service-level invariants
- Internal state structure
- Usage examples for common scenarios

**Next Phase**: Generate quickstart.md
