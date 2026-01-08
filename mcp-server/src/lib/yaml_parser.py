"""YAML frontmatter parsing utilities for markdown command files.

This module provides functions to parse YAML frontmatter and markdown content
from command files using the python-frontmatter library.
"""

from typing import Any

import frontmatter


def parse_command_file(file_path: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter and markdown content from a command file.

    Args:
        file_path: Absolute path to the command file (.md)

    Returns:
        A tuple of (frontmatter_dict, markdown_content):
        - frontmatter_dict: Parsed YAML frontmatter as dictionary
        - markdown_content: Full markdown content including frontmatter and body

    Raises:
        FileNotFoundError: If file_path does not exist
        ValueError: If YAML frontmatter is invalid or malformed

    Examples:
        >>> metadata, content = parse_command_file(".claude/commands/sp.specify.md")
        >>> metadata['description']
        'Create or update the feature specification'
        >>> '$ARGUMENTS' in content
        True
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Extract frontmatter metadata as dictionary
        metadata = post.metadata

        # Get full content (frontmatter + body)
        # We need to preserve the original file content including frontmatter
        with open(file_path, encoding="utf-8") as f:
            full_content = f.read()

        return metadata, full_content

    except FileNotFoundError:
        raise FileNotFoundError(f"Command file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Failed to parse YAML frontmatter in {file_path}: {e}")


def extract_description(metadata: dict[str, Any]) -> str:
    """Extract description from frontmatter metadata.

    Args:
        metadata: Parsed YAML frontmatter dictionary

    Returns:
        Description string (empty string if not present)
    """
    return metadata.get("description", "")


def extract_handoffs(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract handoffs from frontmatter metadata.

    Args:
        metadata: Parsed YAML frontmatter dictionary

    Returns:
        List of handoff dictionaries (empty list if not present)
    """
    return metadata.get("handoffs", [])
