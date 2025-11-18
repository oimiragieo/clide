"""Tests for configuration management."""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from clide.config import Config  # noqa: E402


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.db_path == "memory_bank.db"
    assert config.dashboard_host == "127.0.0.1"
    assert config.dashboard_port == 5000
    assert config.verbose is False


def test_config_from_env():
    """Test configuration from environment variables."""
    os.environ["CLIDE_DB"] = "test.db"
    os.environ["CLIDE_DASHBOARD_HOST"] = "0.0.0.0"
    os.environ["CLIDE_DASHBOARD_PORT"] = "8080"
    os.environ["CLIDE_VERBOSE"] = "true"

    try:
        config = Config()
        assert config.db_path == "test.db"
        assert config.dashboard_host == "0.0.0.0"
        assert config.dashboard_port == 8080
        assert config.verbose is True
    finally:
        # Clean up
        del os.environ["CLIDE_DB"]
        del os.environ["CLIDE_DASHBOARD_HOST"]
        del os.environ["CLIDE_DASHBOARD_PORT"]
        del os.environ["CLIDE_VERBOSE"]


def test_config_db_exists():
    """Test db_exists property."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        os.environ["CLIDE_DB"] = db_path
        config = Config()
        assert config.db_exists is True
    finally:
        del os.environ["CLIDE_DB"]
        Path(db_path).unlink(missing_ok=True)


def test_config_db_not_exists():
    """Test db_exists when database doesn't exist."""
    os.environ["CLIDE_DB"] = "/nonexistent/path/db.db"

    try:
        config = Config()
        assert config.db_exists is False
    finally:
        del os.environ["CLIDE_DB"]


def test_config_validate_no_db():
    """Test validation when database doesn't exist."""
    os.environ["CLIDE_DB"] = "/nonexistent/path/db.db"

    try:
        config = Config()
        is_valid, errors = config.validate()
        assert is_valid is False
        assert len(errors) > 0
        assert "not found" in errors[0].lower()
    finally:
        del os.environ["CLIDE_DB"]


def test_config_validate_with_db():
    """Test validation when database exists."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        os.environ["CLIDE_DB"] = db_path
        config = Config()
        is_valid, errors = config.validate()
        assert is_valid is True
        assert len(errors) == 0
    finally:
        del os.environ["CLIDE_DB"]
        Path(db_path).unlink(missing_ok=True)
