"""Argument sanitization utilities for template injection prevention.

This module provides functions to escape special characters in user input
to prevent template injection attacks.
"""


def sanitize_arguments(arguments: str) -> str:
    """Escape special characters to prevent template injection.

    Security Considerations:
    - Escapes $ → \\$ (prevent variable expansion)
    - Escapes ` → \\` (prevent code execution)
    - Preserves quotes, braces, brackets (safe in markdown)

    Args:
        arguments: Raw user input

    Returns:
        Sanitized input with escaped special chars

    Examples:
        >>> sanitize_arguments("Add $VAR support")
        'Add \\\\$VAR support'

        >>> sanitize_arguments("Add `inline code` support")
        'Add \\\\`inline code\\\\` support'

        >>> sanitize_arguments("Add {braces} and 'quotes'")
        "Add {braces} and 'quotes'"

        >>> sanitize_arguments("")
        ''
    """
    if not arguments:
        return ""

    # Escape $ to prevent variable expansion
    sanitized = arguments.replace("$", "\\$")

    # Escape backticks to prevent code execution
    sanitized = sanitized.replace("`", "\\`")

    # Quotes, braces, and brackets are safe in markdown - preserve them
    return sanitized
