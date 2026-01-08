"""Template processing service for argument interpolation.

This module provides functionality to process prompt templates by
interpolating user arguments into the $ARGUMENTS placeholder.
"""

import logging

from ..models.template import PromptTemplate

logger = logging.getLogger(__name__)


def process_template(template: PromptTemplate, arguments: str) -> str:
    """Process a template by interpolating arguments.

    This function is a thin wrapper around template.interpolate() for
    service-layer abstraction.

    Args:
        template: PromptTemplate object to process
        arguments: User input to interpolate (may be empty)

    Returns:
        Processed template with $ARGUMENTS replaced by sanitized arguments

    Examples:
        >>> template = PromptTemplate(content="Input: $ARGUMENTS", has_arguments=True)
        >>> process_template(template, "Add auth")
        'Input: Add auth'

        >>> process_template(template, "")
        'Input: '
    """
    logger.debug(
        f"Processing template (has_arguments: {template.has_arguments}, "
        f"arg_length: {len(arguments)})"
    )

    processed = template.interpolate(arguments)

    logger.debug(f"Template processed successfully (output_length: {len(processed)})")

    return processed
