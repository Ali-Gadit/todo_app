"""CommandDefinition model for SpecifyPlus commands.

This module defines the CommandDefinition entity representing a SpecifyPlus command
loaded from a `.md` file in `.claude/commands/`.
"""

import re
from dataclasses import dataclass, field

from .handoff import Handoff
from .template import PromptTemplate


@dataclass(frozen=True)
class CommandDefinition:
    """Represents a SpecifyPlus command loaded from a `.md` file.

    Attributes:
        name: Command name (e.g., "sp.specify") - must match pattern sp\\..*
        file_path: Absolute path to source file (must exist and be readable)
        description: Human-readable command description (max 500 chars)
        handoffs: Recommended next steps (empty list if not specified)
        template: Full prompt template (must contain valid markdown)
    """

    name: str
    file_path: str
    description: str
    template: PromptTemplate
    handoffs: list[Handoff] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate command attributes after initialization."""
        # Validate name matches sp.* pattern (sp followed by dot and anything)
        if not re.match(r"^sp\..*", self.name):
            raise ValueError(f"Command name must match pattern 'sp\\..*', got: {self.name}")

        # Validate file_path is non-empty
        if not self.file_path:
            raise ValueError("File path must be non-empty")

        # Validate description is non-empty and within limit
        if not self.description or len(self.description) > 500:
            raise ValueError(
                f"Description must be non-empty and max 500 chars, "
                f"got length: {len(self.description)}"
            )

        # Validate handoffs list (frozen dataclass requires object.__setattr__)
        if not isinstance(self.handoffs, list):
            raise ValueError(f"Handoffs must be a list, got: {type(self.handoffs)}")
