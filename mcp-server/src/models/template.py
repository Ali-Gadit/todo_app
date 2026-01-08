"""PromptTemplate model for markdown templates with argument interpolation.

This module defines the PromptTemplate entity representing the markdown content
of a command file with argument placeholders.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    """Represents the markdown content of a command file with argument placeholders.

    Attributes:
        content: Full markdown including YAML frontmatter and body (non-empty string)
        has_arguments: Whether template contains $ARGUMENTS placeholder
    """

    content: str
    has_arguments: bool

    def __post_init__(self) -> None:
        """Validate template attributes after initialization."""
        if not self.content:
            raise ValueError("Content must be non-empty string")

    def sanitize_arguments(self, arguments: str) -> str:
        """Escape special characters to prevent template injection.

        Security Considerations:
        - Escapes $ → \\$ (prevent variable expansion)
        - Escapes ` → \\` (prevent code execution)
        - Preserves quotes, braces, brackets (safe in markdown)

        Args:
            arguments: Raw user input

        Returns:
            Sanitized input with escaped special chars
        """
        if not arguments:
            return ""

        # Escape $ to prevent variable expansion
        sanitized = arguments.replace("$", "\\$")

        # Escape backticks to prevent code execution
        sanitized = sanitized.replace("`", "\\`")

        return sanitized

    def interpolate(self, arguments: str) -> str:
        """Replace $ARGUMENTS placeholder with user-provided input.

        Edge Cases:
        - Empty arguments: Replace $ARGUMENTS with empty string
        - Multiple $ARGUMENTS: Replace all occurrences
        - No $ARGUMENTS: Return content unchanged

        Args:
            arguments: User input to interpolate (may be empty)

        Returns:
            Template with $ARGUMENTS replaced by sanitized arguments
        """
        sanitized = self.sanitize_arguments(arguments)
        return self.content.replace("$ARGUMENTS", sanitized)
