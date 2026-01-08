"""Main MCP server entry point for SpecifyPlus commands.

This module creates the MCP server instance, loads commands at startup,
and registers MCP protocol handlers (prompts/list, prompts/get).
"""

import asyncio
import logging
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import GetPromptResult, Prompt

from .models.command import CommandDefinition
from .services.command_loader import load_commands
from .services.mcp_handler import get_prompt, list_prompts

# Configure logging to file or stderr (stdout reserved for MCP protocol)
log_file = os.getenv("MCP_LOG_FILE")
if log_file:
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_file,
            filemode="a",
        )
    except Exception:
        # Fallback to stderr if file logging fails
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            stream=sys.stderr,
        )
else:
    # No log file specified, use stderr
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )

logger = logging.getLogger(__name__)

# Global commands dictionary (loaded at startup)
commands: dict[str, CommandDefinition] = {}


def initialize_server() -> Server:
    """Initialize MCP server and load commands.

    Returns:
        Configured Server instance with registered handlers

    Side Effects:
        - Loads commands from .claude/commands/ into global commands dict
        - Logs startup information and loaded command count
    """
    global commands

    logger.info("Starting SpecifyPlus MCP Server...")

    # Determine commands directory path
    # Check environment variable first, then try parent directory, then current directory
    import os
    from pathlib import Path

    commands_dir = os.getenv("COMMANDS_DIR")
    if not commands_dir:
        # Try parent directory first (../.claude/commands)
        parent_dir = Path(__file__).parent.parent.parent / ".claude" / "commands"
        if parent_dir.exists():
            commands_dir = str(parent_dir)
        else:
            # Fall back to current directory
            commands_dir = ".claude/commands"

    logger.info(f"Looking for commands in: {commands_dir}")

    # Load commands from .claude/commands/
    try:
        commands = load_commands(commands_dir)
    except Exception as e:
        logger.error(f"Failed to load commands: {e}", exc_info=True)
        # Continue with empty commands dict - server can still start
        commands = {}

    if not commands:
        logger.warning(
            "No commands loaded. Server will run but have no available prompts. "
            "Ensure .claude/commands/ directory exists with *.md files."
        )
    else:
        logger.info(f"Loaded {len(commands)} commands: {', '.join(sorted(commands.keys()))}")

    # Create MCP server instance
    server = Server("specifyplus-mcp-server")

    # Register prompts/list handler
    @server.list_prompts()
    async def handle_list_prompts() -> list[Prompt]:
        """Handle prompts/list MCP operation.

        Returns:
            List of all available prompts with names, descriptions, and arguments
        """
        return list_prompts(commands)

    # Register prompts/get handler
    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, Any] | None = None
    ) -> GetPromptResult:
        """Handle prompts/get MCP operation.

        Args:
            name: Command name to invoke
            arguments: Command arguments dictionary

        Returns:
            GetPromptResult with description and interpolated template

        Raises:
            ValueError: If command not found
        """
        try:
            description, messages = get_prompt(commands, name, arguments)
            return GetPromptResult(description=description, messages=messages)
        except ValueError as e:
            logger.error(f"Command not found: {name} - {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to get prompt {name}: {e}", exc_info=True)
            raise ValueError(f"Failed to process prompt '{name}': {e}")

    logger.info("Server initialization complete. Ready to accept connections.")
    return server


async def main() -> None:
    """Main entry point for MCP server.

    Initializes server, loads commands, and runs with stdio transport.
    """
    server = initialize_server()

    # Run server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running on stdio. Listening for MCP requests...")
        try:
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            raise


def run() -> None:
    """Synchronous entry point for running the server."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Fatal server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run()
