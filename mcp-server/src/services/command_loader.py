"""Command loader service for SpecifyPlus commands.

This module provides functionality to scan .claude/commands/*.md files,
parse YAML frontmatter, and create CommandDefinition objects.
"""

import logging
import os
from pathlib import Path

from ..lib.yaml_parser import extract_description, extract_handoffs, parse_command_file
from ..models.command import CommandDefinition
from ..models.handoff import Handoff
from ..models.template import PromptTemplate

logger = logging.getLogger(__name__)


def load_commands(commands_dir: str = ".claude/commands") -> dict[str, CommandDefinition]:
    """Load all SpecifyPlus commands from .md files.

    Scans the commands directory for *.md files, parses YAML frontmatter,
    and creates CommandDefinition objects.

    Args:
        commands_dir: Path to directory containing command files (default: .claude/commands)

    Returns:
        Dictionary mapping command names to CommandDefinition objects
        Example: {"sp.specify": CommandDefinition(...), "sp.plan": CommandDefinition(...)}

    Raises:
        Warning (logged): If commands_dir doesn't exist, returns empty dict
        Warning (logged): If individual command files fail to parse, skips them
    """
    commands: dict[str, CommandDefinition] = {}

    # Check if commands directory exists
    commands_path = Path(commands_dir)
    if not commands_path.exists() or not commands_path.is_dir():
        logger.warning(
            f"Commands directory not found: {commands_dir}. Starting with empty command list."
        )
        return commands

    # Scan for .md files
    md_files = list(commands_path.glob("*.md"))
    if not md_files:
        logger.warning(
            f"No command files (*.md) found in {commands_dir}. Starting with empty command list."
        )
        return commands

    logger.info(f"Loading commands from {commands_dir}...")

    # Process each command file
    for md_file in md_files:
        try:
            command = _load_single_command(str(md_file))
            commands[command.name] = command
            logger.debug(f"Loaded command: {command.name} from {md_file.name}")
        except Exception as e:
            logger.error(f"Failed to load command from {md_file.name}: {e}", exc_info=True)
            # Continue loading other commands even if one fails

    logger.info(f"Loaded {len(commands)} commands: {', '.join(commands.keys())}")
    return commands


def _load_single_command(file_path: str) -> CommandDefinition:
    """Load a single command from a .md file.

    Args:
        file_path: Absolute path to the command file

    Returns:
        CommandDefinition object

    Raises:
        ValueError: If file parsing or validation fails
    """
    # Parse YAML frontmatter and markdown content
    metadata, full_content = parse_command_file(file_path)

    # Extract command name from filename (e.g., "sp.specify.md" -> "sp.specify")
    file_name = Path(file_path).name
    command_name = file_name.replace(".md", "")

    # Extract description from frontmatter
    description = extract_description(metadata)
    if not description:
        logger.warning(f"No description found in {file_name}, using empty string")
        description = ""

    # Extract handoffs from frontmatter
    handoffs_data = extract_handoffs(metadata)
    handoffs: list[Handoff] = []
    for handoff_dict in handoffs_data:
        try:
            handoff = Handoff(
                label=handoff_dict.get("label", ""),
                agent=handoff_dict.get("agent", ""),
                prompt=handoff_dict.get("prompt", ""),
                send=handoff_dict.get("send", False),
            )
            handoffs.append(handoff)
        except Exception as e:
            logger.warning(f"Failed to parse handoff in {file_name}: {e}")
            # Continue with other handoffs

    # Create PromptTemplate
    has_arguments = "$ARGUMENTS" in full_content
    template = PromptTemplate(content=full_content, has_arguments=has_arguments)

    # Create CommandDefinition
    command = CommandDefinition(
        name=command_name,
        file_path=os.path.abspath(file_path),
        description=description,
        template=template,
        handoffs=handoffs,
    )

    return command
