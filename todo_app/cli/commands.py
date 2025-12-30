"""CLI command handlers for Todo Console App.

Provides argparse subparsers for all commands:
- add: Add new task
- list: List all tasks
- update: Update task
- complete: Mark task as complete
- incomplete: Mark task as incomplete
- delete: Delete task
"""

import argparse
from todo_app.services.task_service import TaskService
from todo_app.lib.exceptions import TaskNotFound, InvalidTitle


# Status indicators
STATUS_INCOMPLETE: str = "⬜"
STATUS_COMPLETE: str = "✅"


def create_parser() -> argparse.ArgumentParser:
    """Create main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Command-line todo application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task to your todo list",
    )
    add_parser.add_argument(
        "title",
        type=str,
        help="Task title (required)",
    )
    add_parser.add_argument(
        "description",
        type=str,
        nargs="?",
        default="",
        help="Optional task description",
    )

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks with status indicators",
    )

    # Update command
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing task's title and/or description",
    )
    update_parser.add_argument(
        "id",
        type=int,
        help="Task ID to update",
    )
    update_parser.add_argument(
        "title",
        type=str,
        help="New task title (required)",
    )
    update_parser.add_argument(
        "description",
        type=str,
        nargs="?",
        help="New task description (optional)",
    )

    # Complete command
    complete_parser = subparsers.add_parser(
        "complete",
        help="Mark a task as completed",
    )
    complete_parser.add_argument(
        "id",
        type=int,
        help="Task ID to mark complete",
    )

    # Incomplete command
    incomplete_parser = subparsers.add_parser(
        "incomplete",
        help="Mark a task as incomplete",
    )
    incomplete_parser.add_argument(
        "id",
        type=int,
        help="Task ID to mark incomplete",
    )

    # Delete command
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task from your todo list",
    )
    delete_parser.add_argument(
        "id",
        type=int,
        help="Task ID to delete",
    )

    return parser


def add_task_cmd(service: TaskService, args: argparse.Namespace) -> None:
    """Handle 'add' command.

    Adds a new task with title and optional description.
    Displays success message with task ID or error message.
    """
    try:
        task = service.add_task(args.title, args.description or "")
        print(f"✓ Task added successfully (ID: {task.id})")
    except InvalidTitle as e:
        print(f"✗ Error: {e}")


def list_tasks_cmd(service: TaskService, args: argparse.Namespace) -> None:
    """Handle 'list' command.

    Displays all tasks with ID, title, description, and status indicator.
    Shows empty list message if no tasks exist.
    """
    tasks = service.list_tasks()

    if not tasks:
        print("Your Tasks:")
        print("─" * 40)
        print("No tasks found. Add a task with 'todo add <title>'")
        print("─" * 40)
        return

    # Count completed/incomplete
    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count

    print("Your Tasks:")
    print("─" * 40)

    for task in tasks:
        status = STATUS_COMPLETE if task.completed else STATUS_INCOMPLETE
        print(f"[{task.id}] {status} {task.title}")

        if task.description:
            print(f"    {task.description}")

    print("─" * 40)
    print(f"{len(tasks)} tasks total ({completed_count} completed, {pending_count} pending)")


def update_task_cmd(service: TaskService, args: argparse.Namespace) -> None:
    """Handle 'update' command.

    Updates task title and/or description by ID.
    Displays success message or error message.
    """
    try:
        service.update_task(args.id, args.title, args.description)
        print(f"✓ Task {args.id} updated successfully")
    except TaskNotFound as e:
        print(f"✗ Error: {e}")
    except InvalidTitle as e:
        print(f"✗ Error: {e}")


def complete_cmd(service: TaskService, args: argparse.Namespace) -> None:
    """Handle 'complete' command.

    Marks a task as completed.
    Displays success message or error message.
    """
    try:
        service.mark_complete(args.id)
        print(f"✓ Task {args.id} marked as complete")
    except TaskNotFound as e:
        print(f"✗ Error: {e}")


def incomplete_cmd(service: TaskService, args: argparse.Namespace) -> None:
    """Handle 'incomplete' command.

    Marks a task as incomplete.
    Displays success message or error message.
    """
    try:
        service.mark_incomplete(args.id)
        print(f"✓ Task {args.id} marked as incomplete")
    except TaskNotFound as e:
        print(f"✗ Error: {e}")


def delete_task_cmd(service: TaskService, args: argparse.Namespace) -> None:
    """Handle 'delete' command.

    Deletes a task by ID.
    Displays success message or error message.
    """
    try:
        service.delete_task(args.id)
        print(f"✓ Task {args.id} deleted successfully")
    except TaskNotFound as e:
        print(f"✗ Error: {e}")


# Command handler mapping
COMMAND_HANDLERS = {
    "add": add_task_cmd,
    "list": list_tasks_cmd,
    "update": update_task_cmd,
    "complete": complete_cmd,
    "incomplete": incomplete_cmd,
    "delete": delete_task_cmd,
}


def execute_command(service: TaskService, args: argparse.Namespace) -> None:
    """Execute the specified command.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Raises:
        SystemExit: If command is not recognized
    """
    handler = COMMAND_HANDLERS.get(args.command)
    if handler:
        handler(service, args)
    else:
        print(f"Unknown command: {args.command}")
        print("Use 'todo help' to see available commands")
        exit(1)
