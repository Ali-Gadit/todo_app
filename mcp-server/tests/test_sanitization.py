"""Test special characters handling and sanitization."""

import pytest

from src.lib.sanitizer import sanitize_arguments
from src.models.template import PromptTemplate


def test_sanitize_dollar_signs():
    """Test that $ characters are escaped."""
    result = sanitize_arguments("Add $VAR support")
    assert result == "Add \\$VAR support"


def test_sanitize_backticks():
    """Test that backticks are escaped."""
    result = sanitize_arguments("Add `inline code` support")
    assert result == "Add \\`inline code\\` support"


def test_preserve_braces_and_quotes():
    """Test that braces and quotes are preserved."""
    result = sanitize_arguments("Add {braces} and 'quotes' and \"double\"")
    assert result == "Add {braces} and 'quotes' and \"double\""


def test_combined_special_chars():
    """Test combined special characters."""
    result = sanitize_arguments("Test $VAR and `code` and {obj} and 'str'")
    assert result == "Test \\$VAR and \\`code\\` and {obj} and 'str'"


def test_empty_arguments():
    """Test empty arguments."""
    result = sanitize_arguments("")
    assert result == ""


def test_template_interpolation_with_special_chars():
    """Test template interpolation escapes special characters."""
    template = PromptTemplate(content="Input: $ARGUMENTS", has_arguments=True)
    result = template.interpolate("Add $VAR and `code`")
    # Verify $ and ` are escaped
    assert "\\$VAR" in result
    assert "\\`code\\`" in result
    assert result == "Input: Add \\$VAR and \\`code\\`"


def test_template_without_arguments():
    """Test template without $ARGUMENTS placeholder."""
    template = PromptTemplate(content="Static content", has_arguments=False)
    result = template.interpolate("Some input")
    assert result == "Static content"


def test_template_with_empty_arguments():
    """Test template with empty arguments."""
    template = PromptTemplate(content="Input: $ARGUMENTS\nEnd", has_arguments=True)
    result = template.interpolate("")
    assert result == "Input: \nEnd"
