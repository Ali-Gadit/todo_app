# Data Model: Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Purpose**: Define data entities, validation rules, and state transitions

## Entities

### Task

**Purpose**: Represents a single todo item with unique identifier, title, description, and completion status.

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|-----------|-------------|-------------|
| id | int | Yes | Unique sequential numeric identifier (starting from 1) | Must be positive integer, unique |
| title | str | Yes | Task title/name | Non-empty string, max 1000 chars, supports unicode |
| description | str | No | Optional task details | Optional, max 1000 chars, supports unicode |
| completed | bool | No | Task completion status | True/False, defaults to False |

**Python Representation** (dataclass):

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

## Invariants & Constraints

### Task Entity Invariants

| Invariant | Rule | Enforcement Point |
|-----------|------|-------------------|
| T-001 | Task ID must be positive integer | Task creation in service layer |
| T-002 | Task ID must be unique | Task creation, ID generation |
| T-003 | Title must be non-empty string | Task creation, update validation |
| T-004 | Title length <= 1000 characters | Task creation, update validation |
| T-005 | Description length <= 1000 characters | Task creation, update validation |
| T-006 | completed status is boolean | Task creation, update, complete/incomplete operations |
| T-007 | IDs are stable on delete | Delete operation (no renumbering) |

---

## State Transitions

### Task Lifecycle States

```
[Created] → [Incomplete] → [Complete]
                              ↓
                          [Incomplete] (toggle back)
```

**Transition Rules**:

| Current State | Operation | New State | Precondition |
|--------------|-----------|------------|---------------|
| N/A | Create Task | Incomplete | Title non-empty |
| Incomplete | Mark Complete | Complete | Task exists |
| Incomplete | Update (title/description) | Incomplete | Task exists, title non-empty if updated |
| Complete | Mark Incomplete | Incomplete | Task exists |
| Complete | Update (title/description) | Complete | Task exists, title non-empty if updated |
| Any | Delete | Removed | Task exists |

**Forbidden Transitions**:

| Attempt | Reason | Exception |
|----------|--------|-------------|
| Create task with empty title | Violates FR-005 | InvalidTitle |
| Update task to empty title | Violates FR-005 | InvalidTitle |
| Update non-existent task | Violates FR-009 | TaskNotFound |
| Mark complete non-existent task | Violates FR-009 | TaskNotFound |
| Mark incomplete non-existent task | Violates FR-009 | TaskNotFound |
| Delete non-existent task | Violates FR-009 | TaskNotFound |

---

## Storage Model

### In-Memory Collection

**Structure**: Single list of Task objects ordered by creation time (ID order).

```python
# In-memory task storage
tasks: list[Task] = []
next_id: int = 1  # Sequential ID counter
```

**Operations**:

| Operation | Description | Complexity |
|-----------|-------------|------------|
| add(title, description) | Append new task, increment next_id | O(1) |
| get_by_id(id) | Linear search for task by ID | O(n) |
| update(id, title, description) | Search, modify task | O(n) |
| mark_complete(id) | Search, toggle completed | O(n) |
| delete(id) | Search, remove task | O(n) |
| list_all() | Return all tasks (ordered) | O(n) |

**Rationale**:
- Simple list structure aligns with Principle IV (Simple Architecture)
- O(n) operations acceptable for expected scale (<100 tasks)
- No indexing overhead for small dataset
- Direct iteration for display operations

---

## Exception Hierarchy

### Custom Exception Types

```python
# Domain-specific exceptions
class TaskNotFound(Exception):
    """Raised when task ID does not exist in task list."""
    pass

class InvalidTitle(Exception):
    """Raised when task title is empty or exceeds length limit."""
    pass
```

**Usage Pattern**:

```python
try:
    task_service.mark_complete(task_id)
except TaskNotFound:
    print("Error: Task not found. Please check the task ID.")
except InvalidTitle as e:
    print(f"Error: {e}")
```

---

## Validation Rules

### Input Validation

| Input | Rule | Error Type | User Message |
|--------|------|-------------|---------------|
| Empty title | Must have 1+ characters | InvalidTitle | "Error: Task title cannot be empty" |
| Title > 1000 chars | Must be <= 1000 characters | InvalidTitle | "Error: Task title exceeds maximum length (1000 characters)" |
| Description > 1000 chars | Must be <= 1000 characters | InvalidTitle | "Error: Task description exceeds maximum length (1000 characters)" |
| Task ID not found | Must exist in task list | TaskNotFound | "Error: Task with ID {id} not found" |

---

## Unicode & Special Character Support

**Support**: Full unicode and special character support (including emojis)

**Rationale**:
- FR-015: "System MUST support special characters and unicode in task titles and descriptions"
- Python 3.13+ handles unicode natively
- No special encoding required

**Valid Examples**:
- Title: "Buy groceries 🛒"
- Description: "Meeting at café ☕"
- Special chars: "Fix bug #123", "Urgent!!!"

---

## Edge Cases

### Boundary Conditions

| Case | Behavior | Implementation Notes |
|-------|----------|--------------------|
| Empty task list | Returns empty list, displays "No tasks found" message | FR-014 |
| Max title length (1000 chars) | Accepts, validates at 1000 | Truncate or reject? Accept per spec |
| Max description length (1000 chars) | Accepts, validates at 1000 | Same as title |
| First task (ID=1) | next_id=1, ID assigned as 1 | Initial state |
| Delete last remaining task | tasks list becomes empty | Handle empty state |
| Duplicate titles | Allowed (different IDs) | Titles not required to be unique |

### Rapid Operations

| Scenario | Behavior | Implementation Notes |
|----------|----------|--------------------|
| Add then immediately delete | Task added, ID assigned, then removed | ID not reused (stable IDs) |
| Mark complete then mark incomplete | Toggles back to incomplete | Normal operation |
| Update non-existent task | Raises TaskNotFound | Clear error message |

---

## Summary

Data model is complete with:
- Task entity (4 fields with validation)
- 7 invariants for data integrity
- State transition rules (6 valid, 6 forbidden)
- In-memory list storage with O(n) operations
- 2 custom exception types
- Input validation for 4 edge cases
- Full unicode support

**Next Phase**: Generate contracts/ and quickstart.md
