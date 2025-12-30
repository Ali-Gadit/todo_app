# CLI Commands Contract: Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Purpose**: Define command-line interface contract

## Command Structure

**Base Command**: `todo` (or `python -m todo_app.cli.main`)

```
Usage: todo <command> [arguments]

Commands:
  add <title> [description]    Add a new task
  list                           List all tasks
  update <id> <title> [desc]    Update task by ID
  complete <id>                 Mark task as complete
  incomplete <id>               Mark task as incomplete
  delete <id>                   Delete task by ID
  help                           Show help message
```

---

## Command Contracts

### 1. add

Add a new task to the todo list.

**Syntax**:
```
todo add <title> [description]
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| title | string | Yes | Non-empty, <=1000 chars |
| description | string | No | Optional, <=1000 chars |

**Success Output**:
```
✓ Task added successfully (ID: 1)
```

**Error Output**:
```
✗ Error: Task title cannot be empty
```

---

### 2. list

Display all tasks in the todo list.

**Syntax**:
```
todo list
```

**Parameters**: None

**Success Output (with tasks)**:
```
Your Tasks:
────────────────────────────────────────

[1] ⬜ Buy groceries
    Weekly shopping at the supermarket

[2] ✅ Complete project report
    Due by Friday

[3] ⬜ Call doctor
    Schedule annual checkup

────────────────────────────────────────
3 tasks total (1 completed, 2 pending)
```

**Success Output (empty)**:
```
Your Tasks:
────────────────────────────────────────

No tasks found. Add a task with 'todo add <title>'

────────────────────────────────────────
```

**Legend**:
- `⬜` - Incomplete task
- `✅` - Completed task

---

### 3. update

Update an existing task's title and/or description.

**Syntax**:
```
todo update <id> <new_title> [new_description]
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| id | integer | Yes | Positive integer, task must exist |
| new_title | string | Yes | Non-empty, <=1000 chars |
| new_description | string | No | Optional, <=1000 chars |

**Success Output**:
```
✓ Task 1 updated successfully
```

**Error Output**:
```
✗ Error: Task with ID 1 not found
```

```
✗ Error: Task title cannot be empty
```

---

### 4. complete

Mark a task as completed.

**Syntax**:
```
todo complete <id>
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| id | integer | Yes | Positive integer, task must exist |

**Success Output**:
```
✓ Task 1 marked as complete
```

**Error Output**:
```
✗ Error: Task with ID 1 not found
```

---

### 5. incomplete

Mark a task as incomplete.

**Syntax**:
```
todo incomplete <id>
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| id | integer | Yes | Positive integer, task must exist |

**Success Output**:
```
✓ Task 1 marked as incomplete
```

**Error Output**:
```
✗ Error: Task with ID 1 not found
```

---

### 6. delete

Delete a task from the todo list.

**Syntax**:
```
todo delete <id>
```

**Parameters**:
| Parameter | Type | Required | Validation |
|-----------|------|----------|-------------|
| id | integer | Yes | Positive integer, task must exist |

**Success Output**:
```
✓ Task 1 deleted successfully
```

**Error Output**:
```
✗ Error: Task with ID 1 not found
```

**Note**: Deleting a task does not renumber remaining task IDs.

---

### 7. help

Display help message with command usage.

**Syntax**:
```
todo help
```

**Parameters**: None

**Output**: Shows full command syntax and examples.

---

## Command Exit Codes

| Exit Code | Meaning |
|----------|---------|
| 0 | Success |
| 1 | Invalid command or arguments |
| 2 | Task not found |
| 3 | Invalid input (empty title, etc.) |

---

## Examples

### Adding Tasks
```
$ todo add "Buy groceries"
✓ Task added successfully (ID: 1)

$ todo add "Complete project" "Due by Friday"
✓ Task added successfully (ID: 2)

$ todo add "Call doctor"
✓ Task added successfully (ID: 3)
```

### Viewing Tasks
```
$ todo list
Your Tasks:
────────────────────────────────────────

[1] ⬜ Buy groceries
    Weekly shopping at the supermarket

[2] ⬜ Complete project
    Due by Friday

[3] ⬜ Call doctor
    Schedule annual checkup

────────────────────────────────────────
3 tasks total (0 completed, 3 pending)
```

### Updating Tasks
```
$ todo update 1 "Buy groceries 🛒"
✓ Task 1 updated successfully

$ todo update 2 "Complete project report" "Due by Friday 5pm"
✓ Task 2 updated successfully
```

### Marking Complete/Incomplete
```
$ todo complete 2
✓ Task 2 marked as complete

$ todo list
Your Tasks:
────────────────────────────────────────

[1] ⬜ Buy groceries 🛒
    Weekly shopping at the supermarket

[2] ✅ Complete project report
    Due by Friday 5pm

[3] ⬜ Call doctor
    Schedule annual checkup

────────────────────────────────────────
3 tasks total (1 completed, 2 pending)

$ todo incomplete 2
✓ Task 2 marked as incomplete
```

### Deleting Tasks
```
$ todo delete 3
✓ Task 3 deleted successfully

$ todo list
Your Tasks:
────────────────────────────────────────

[1] ⬜ Buy groceries 🛒
    Weekly shopping at the supermarket

[2] ⬜ Complete project report
    Due by Friday 5pm

────────────────────────────────────────
2 tasks total (0 completed, 2 pending)
```
