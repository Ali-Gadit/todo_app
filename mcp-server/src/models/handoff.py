"""Handoff model for workflow progression suggestions.

This module defines the Handoff entity representing a recommended next step
in the Spec-Driven Development workflow.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Handoff:
    """Represents a recommended next step in the Spec-Driven Development workflow.

    Attributes:
        label: Display name for the handoff (max 100 chars)
        agent: Target command name (must match existing command)
        prompt: Suggested prompt text for next command (max 500 chars)
        send: Whether to auto-send the handoff (defaults to False)
    """

    label: str
    agent: str
    prompt: str
    send: bool = False

    def __post_init__(self) -> None:
        """Validate handoff attributes after initialization."""
        if not self.label or len(self.label) > 100:
            raise ValueError(f"Label must be non-empty and max 100 chars, got: {self.label}")
        if not self.agent:
            raise ValueError("Agent must be non-empty")
        if not self.prompt or len(self.prompt) > 500:
            raise ValueError(
                f"Prompt must be non-empty and max 500 chars, got length: {len(self.prompt)}"
            )
