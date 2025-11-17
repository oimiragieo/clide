"""Tests for database functionality."""

import sys
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from clide.db import Database  # noqa: E402


def test_database_creation():
    """Test database creation."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    db = Database(db_path)
    assert db.db_path == db_path

    # Cleanup
    Path(db_path).unlink(missing_ok=True)


def test_trace_id_generation():
    """Test trace ID generation."""
    db = Database(":memory:")
    trace_id = db.generate_trace_id()
    assert isinstance(trace_id, str)
    assert len(trace_id) == 36  # UUID format
