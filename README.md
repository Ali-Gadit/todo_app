# Todo Console App

A command-line todo application that stores tasks in memory.

## Features

- Add tasks with title and optional description
- View all tasks with status indicators (complete/incomplete)
- Update task titles and descriptions
- Mark tasks as complete or incomplete
- Delete tasks by ID

## Installation

### Prerequisites

- Python 3.13 or later
- UV package manager

### Setup

```bash
# Clone repository
git clone <repository-url>
cd todo_app

# Install dependencies with UV (installs 'todo' command)
uv sync

# Run the application using the entry point alias
uv run todo list

# Or run using python module syntax
python -m todo_app.cli.main list
```

## Usage

Recommended usage is via `uv run todo <command>`.

### Adding Tasks

Add a task with title and optional description:

```bash
uv run todo add "Buy groceries"
```

```bash
uv run todo add "Complete project report" "Due by Friday"
```

### Viewing Tasks

List all tasks with status indicators:

```bash
uv run todo list
```

**Output Example**:

```
Your Tasks:
────────────────────────────────────────

[1] ⬜ Buy groceries
    Weekly shopping at supermarket

[2] ⬜ Complete project report
    Due by Friday

[3] ⬜ Call doctor
    Schedule annual checkup

────────────────────────────────────────
3 tasks total (0 completed, 3 pending)
```

**Legend**:
- `⬜` - Incomplete task
- `✅` - Completed task

### Updating Tasks

Update task title and/or description:

```bash
uv run todo update 1 "Buy groceries 🛒"
```

```bash
uv run todo update 2 "Complete project report" "Due by Friday 5pm"
```

### Marking Tasks Complete/Incomplete

Toggle task completion status:

```bash
# Mark as complete
uv run todo complete 2

# Mark as incomplete
uv run todo incomplete 2
```

### Deleting Tasks

Remove a task from your list:

```bash
uv run todo delete 3
```

## Command Reference

```
Usage: uv run todo <command> [arguments]

Commands:
  add <title> [description]    Add a new task
  list                           List all tasks
  update <id> <title> [desc]    Update task by ID
  complete <id>                 Mark task as complete
  incomplete <id>               Mark task as incomplete
  delete <id>                   Delete task by ID
  help                           Show help message
```

## Task IDs

- Task IDs are sequential numbers starting from 1
- Deleting a task does not renumber remaining task IDs
- This ensures stability - task IDs remain consistent

## Development

### Code Quality

```bash
# Check linting issues
uv run ruff check

# Auto-format code
uv run ruff format

# Type checking
uv run pyright

# Run tests (when implemented)
uv run pytest
```

### Project Structure

```
todo_app/
├── src/
│   ├── models/
│   │   └── task.py          # Task entity dataclass
│   ├── services/
│   │   └── task_service.py  # Task CRUD operations
│   ├── cli/
│   │   ├── commands.py       # Command handlers
│   │   └── main.py          # Entry point
│   └── lib/
│       └── exceptions.py    # Custom exceptions
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
├── specs/                       # Feature specifications
├── pyproject.toml               # UV configuration
└── README.md                   # This file
```

## Error Messages

The application provides clear, actionable error messages:

- **Task title cannot be empty** - When adding or updating a task without a title
- **Task title exceeds maximum length (1000 characters)** - When title is too long
- **Task description exceeds maximum length (1000 characters)** - When description is too long
- **Task with ID {id} not found** - When attempting to update, complete, or delete a non-existent task
- **Unknown command** - When using an invalid command

## Examples

### Complete Workflow

```bash
# Add tasks
todo add "Setup development environment"
todo add "Write feature specification"
todo add "Create implementation plan"

# View tasks
todo list
# Output shows 3 tasks

# Mark one as complete
todo complete 1

# View updated list
todo list
# Output shows task 1 with ✅ status

# Update another task
todo update 2 "Write feature specification" "Due by EOD"

# Delete a task
todo delete 3

# Final view
todo list
# Output shows 2 tasks (1 complete, 1 incomplete)
```

## Technology

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Storage**: In-memory (Python data structures)
- **Linting**: Ruff
- **Type Checking**: pyright

## License

[Add your license here]
