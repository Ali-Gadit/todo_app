"""Main entry point for Todo Console App.

Initializes TaskService and routes CLI commands.
"""

import sys
from pathlib import Path

from todo_app.services.task_service import TaskService
from todo_app.cli.commands import create_parser, execute_command


def main() -> None:
    """Main entry point for Todo Console App.

    Initializes TaskService, parses command-line arguments,
    and executes the requested command.
    """
    # Initialize task service
    task_service = TaskService()

    # Create argument parser
    parser = create_parser()

    # Parse arguments
    args = parser.parse_args()

    # Execute command
    execute_command(task_service, args)


if __name__ == "__main__":
    main()
