"""Tests for CLI functionality."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from clide import __version__  # noqa: E402


def test_version():
    """Test version is set."""
    assert __version__ == "1.1.0"


def test_cli_import():
    """Test CLI module can be imported."""
    from clide.cli import cli

    assert cli is not None
