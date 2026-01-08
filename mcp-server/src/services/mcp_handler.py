"""MCP protocol handlers for SpecifyPlus commands.

This module provides MCP protocol operations (prompts/list, prompts/get)
for exposing SpecifyPlus commands as prompts.
"""

import logging
from typing import Any

from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent

from ..models.command import CommandDefinition

logger = logging.getLogger(__name__)


def list_prompts(commands: dict[str, CommandDefinition]) -> list[Prompt]:
    """List all available SpecifyPlus commands as MCP prompts.

    Implements the prompts/list MCP operation.

    Args:
        commands: Dictionary of loaded commands (name -> CommandDefinition)

    Returns:
        List of Prompt objects with name, description, and arguments

    Examples:
        >>> commands = {"sp.specify": CommandDefinition(...)}
        >>> prompts = list_prompts(commands)
        >>> prompts[0].name
        'sp.specify'
        >>> prompts[0].description
        'Create or update the feature specification...'
    """
    prompts: list[Prompt] = []

    for cmd_name, cmd_def in commands.items():
        # Create prompt argument (all commands accept optional feature_description)
        argument = PromptArgument(
            name="feature_description",
            description="Input for the command (optional)",
            required=False,
        )

        # Enhance description with handoffs information if available
        enhanced_description = cmd_def.description
        if cmd_def.handoffs:
            handoff_summary = ", ".join([h.agent for h in cmd_def.handoffs])
            enhanced_description = (
                f"{cmd_def.description} (Suggested next steps: {handoff_summary})"
            )

        # Create Prompt object
        prompt = Prompt(
            name=cmd_name,
            description=enhanced_description,
            arguments=[argument] if cmd_def.template.has_arguments else [],
        )

        prompts.append(prompt)
        logger.debug(f"Listed prompt: {cmd_name}")

    logger.info(f"Returned {len(prompts)} prompts via prompts/list")
    return prompts


def get_prompt(
    commands: dict[str, CommandDefinition], name: str, arguments: dict[str, Any] | None = None
) -> tuple[str, list[PromptMessage]]:
    """Get a specific prompt with argument interpolation.

    Implements the prompts/get MCP operation.

    Args:
        commands: Dictionary of loaded commands (name -> CommandDefinition)
        name: Command name to invoke (e.g., "sp.specify")
        arguments: Arguments dictionary (e.g., {"feature_description": "Add auth"})

    Returns:
        Tuple of (description, messages):
        - description: Command description
        - messages: List of PromptMessage with interpolated template

    Raises:
        ValueError: If command not found

    Examples:
        >>> commands = {"sp.specify": CommandDefinition(...)}
        >>> desc, msgs = get_prompt(commands, "sp.specify", {"feature_description": "Add auth"})
        >>> desc
        'Create or update the feature specification...'
        >>> msgs[0].role
        'user'
        >>> '$ARGUMENTS' in msgs[0].content.text
        False
    """
    # Look up command
    if name not in commands:
        available_commands = ", ".join(commands.keys())
        raise ValueError(f"Command '{name}' not found. Available commands: {available_commands}")

    cmd_def = commands[name]

    # Extract user input from arguments
    if arguments is None:
        arguments = {}

    user_input = arguments.get("feature_description", "")

    # Interpolate template with arguments
    interpolated_content = cmd_def.template.interpolate(user_input)

    # Create PromptMessage
    message = PromptMessage(
        role="user", content=TextContent(type="text", text=interpolated_content)
    )

    logger.info(
        f"Invoked prompt: {name} with arguments (preview): "
        f"{user_input[:100]}{'...' if len(user_input) > 100 else ''}"
    )

    return cmd_def.description, [message]
