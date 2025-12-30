# Quickstart: Todo Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Purpose**: Quick setup and validation guide for Todo Console App

## Overview

The Todo Console App is a command-line todo application that stores tasks in memory. It supports adding, viewing, updating, completing, and deleting tasks through a simple CLI interface.

## Prerequisites

- Python 3.13 or later
- UV package manager (for project setup)

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo_app
git checkout 001-todo-console-app
```

### 2. Install Dependencies with UV

```bash
# Create virtual environment and install dependencies
uv sync

# Or if pyproject.toml not yet created:
uv init
uv add pytest
```

### 3. Verify Installation

```bash
# Check Python version
python --version
# Expected output: Python 3.13.x

# Run pytest to verify test framework
uv run pytest --version
# Expected output: pytest 8.x.x
```

---

## Running the Application

### Launch Todo App

```bash
# Run from project root
python -m todo_app.cli.main

# Or if entry point is configured:
todo
```

### View Help

```bash
todo help
```

**Output**:
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

## Basic Usage

### Adding Tasks

Add a task with title and optional description:

```bash
todo add "Buy groceries"
# Output: ✓ Task added successfully (ID: 1)

todo add "Complete project report" "Due by Friday"
# Output: ✓ Task added successfully (ID: 2)
```

### Viewing Tasks

List all tasks with status indicators:

```bash
todo list
```

**Output**:
```
Your Tasks:
────────────────────────────────────────

[1] ⬜ Buy groceries
    Weekly shopping at supermarket

[2] ⬜ Complete project report
    Due by Friday

────────────────────────────────────────
2 tasks total (0 completed, 2 pending)
```

**Legend**:
- `⬜` - Incomplete task
- `✅` - Completed task

### Updating Tasks

Update task title and/or description:

```bash
todo update 1 "Buy groceries 🛒"
# Output: ✓ Task 1 updated successfully

todo update 2 "Complete project report" "Due by Friday 5pm"
# Output: ✓ Task 2 updated successfully
```

### Marking Tasks Complete/Incomplete

Toggle task completion status:

```bash
todo complete 2
# Output: ✓ Task 2 marked as complete

todo list
# Shows: [2] ✅ Complete project report

todo incomplete 2
# Output: ✓ Task 2 marked as incomplete
```

### Deleting Tasks

Remove a task from the list:

```bash
todo delete 1
# Output: ✓ Task 1 deleted successfully

todo list
# Shows: [2] ⬜ Complete project report (ID remains 2, not renumbered)
```

---

## Complete Example Workflow

```bash
# Start with empty task list
todo list
# Output: No tasks found. Add a task with 'todo add <title>'

# Add first task
todo add "Setup development environment"
# Output: ✓ Task added successfully (ID: 1)

# Add second task
todo add "Write feature specification"
# Output: ✓ Task added successfully (ID: 2)

# Add third task
todo add "Create implementation plan"
# Output: ✓ Task added successfully (ID: 3)

# View all tasks
todo list
# Output:
# Your Tasks:
# ────────────────────────────────────────
# [1] ⬜ Setup development environment
# [2] ⬜ Write feature specification
# [3] ⬜ Create implementation plan
# ────────────────────────────────────────
# 3 tasks total (0 completed, 3 pending)

# Mark first task complete
todo complete 1
# Output: ✓ Task 1 marked as complete

# View updated list
todo list
# Shows: [1] ✅ Setup development environment

# Update second task
todo update 2 "Write feature specification" "Due by EOD"
# Output: ✓ Task 2 updated successfully

# Delete third task
todo delete 3
# Output: ✓ Task 3 deleted successfully

# Final view
todo list
# Output:
# Your Tasks:
# ────────────────────────────────────────
# [1] ✅ Setup development environment
# [2] ⬜ Write feature specification
#     Due by EOD
# ────────────────────────────────────────
# 2 tasks total (1 completed, 1 pending)
```

---

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test File

```bash
uv run pytest tests/unit/test_task_model.py
```

### Run with Verbose Output

```bash
uv run pytest -v
```

---

## Project Structure

```
todo_app/
├── src/
│   ├── models/
│   │   └── task.py              # Task entity
│   ├── services/
│   │   └── task_service.py       # Task CRUD operations
│   ├── cli/
│   │   ├── commands.py           # Command handlers
│   │   └── main.py              # Entry point
│   └── lib/
│       └── exceptions.py         # Custom exceptions
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
├── specs/
│   └── 001-todo-console-app/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md            # This file
│       ├── contracts/
│       └── tasks.md
└── pyproject.toml                 # UV configuration
```

---

## Code Quality

### Run Linter

```bash
# Check for linting issues
uv run ruff check

# Auto-fix formatting
uv run ruff format
```

### Type Checking

```bash
# Run static type checker
uv run pyright
```

---

## Common Issues

### Task ID Not Found

**Error**:
```
✗ Error: Task with ID 999 not found
```

**Solution**: Check your task list with `todo list` to see valid task IDs.

### Empty Title

**Error**:
```
✗ Error: Task title cannot be empty
```

**Solution**: Provide a non-empty title when adding or updating tasks.

### Long Input Truncated

**Error**:
```
✗ Error: Task title exceeds maximum length (1000 characters)
```

**Solution**: Keep titles and descriptions under 1000 characters.

---

## Next Steps

After completing quickstart:

1. Review [data-model.md](./data-model.md) for entity structure
2. Review [contracts/](./contracts/) for detailed interface specifications
3. Review [plan.md](./plan.md) for implementation strategy
4. Run `/sp.tasks` to generate task breakdown for implementation

---

## Validation Checklist

Use this checklist to validate the application works as expected:

- [ ] Application launches without errors
- [ ] Can add a task with title only
- [ ] Can add a task with title and description
- [ ] Can view list of all tasks
- [ ] Empty list shows "No tasks found" message
- [ ] Can update task title
- [ ] Can update task description
- [ ] Can mark task as complete
- [ ] Can mark task as incomplete
- [ ] Can delete a task
- [ ] Status indicators display correctly (⬜, ✅)
- [ ] Task IDs remain stable after deletion
- [ ] Error messages are clear and actionable
- [ ] Special characters and emojis are supported
- [ ] All tests pass: `uv run pytest`
- [ ] Linter passes: `uv run ruff check`
- [ ] Type checker passes: `uv run pyright`

**All items checked**: Application is ready for use.

---

## Support

For issues or questions:
1. Check [spec.md](./spec.md) for requirements
2. Check [data-model.md](./data-model.md) for data structure
3. Check [contracts/](./contracts/) for interface details
4. Review error messages - they provide actionable guidance
