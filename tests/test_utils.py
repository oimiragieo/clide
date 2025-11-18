"""Tests for utility functions."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from clide.utils import format_datetime, format_priority, truncate  # noqa: E402


def test_format_priority():
    """Test priority formatting."""
    assert "Critical" in format_priority(1)
    assert "High" in format_priority(2)
    assert "Medium" in format_priority(3)
    assert "Low" in format_priority(4)


def test_truncate():
    """Test text truncation."""
    short_text = "Short"
    assert truncate(short_text, 10) == "Short"

    long_text = "This is a very long text that needs truncation"
    result = truncate(long_text, 20)
    assert len(result) <= 23  # 20 + "..."
    assert result.endswith("...")


def test_truncate_empty():
    """Test truncating empty text."""
    assert truncate("", 10) == ""
    assert truncate(None, 10) == ""


def test_format_datetime():
    """Test datetime formatting."""
    # Test with ISO format
    dt = "2025-11-18T10:30:00"
    result = format_datetime(dt)
    assert "2025-11-18" in result

    # Test with empty string
    assert format_datetime("") == ""
    assert format_datetime(None) == ""
