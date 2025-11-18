"""Tests for command implementations."""

import sys
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from clide.commands.save import append_to_agents_log  # noqa: E402
from clide.db import Database  # noqa: E402


def test_append_to_agents_log():
    """Test appending to agents_log.md file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        import os

        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(tmpdir)

        try:
            # Test creating new file
            result = append_to_agents_log("[Test] Test message")
            assert result is True

            log_file = Path("agents_log.md")
            assert log_file.exists()

            content = log_file.read_text()
            assert "# Agents Log" in content
            assert "[Test] Test message" in content

            # Test appending to existing file
            result = append_to_agents_log("[Test] Second message")
            assert result is True

            content = log_file.read_text()
            assert "[Test] Second message" in content
        finally:
            os.chdir(original_dir)


def test_database_story_operations():
    """Test story create and retrieval."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        db = Database(db_path)
        db.initialize()

        # Create a story
        story_id = db.create_story(
            title="Test story", description="Test description", priority=1, assignee="alice"
        )

        assert story_id is not None
        assert story_id > 0

        # Get open stories
        stories = db.get_open_stories()
        assert len(stories) > 0
        assert stories[0]["title"] == "Test story"
        assert stories[0]["assignee"] == "alice"
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_database_defect_operations():
    """Test defect create and resolve."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        db = Database(db_path)
        db.initialize()

        # Create a defect
        defect_id = db.create_defect(
            title="Test defect", description="Test bug", severity="critical", detected_by="user"
        )

        assert defect_id is not None
        assert defect_id > 0

        # Get open defects
        defects = db.get_open_defects()
        assert len(defects) > 0
        assert defects[0]["title"] == "Test defect"
        assert defects[0]["severity"] == "critical"

        # Resolve defect
        db.resolve_defect(defect_id, "Fixed the issue", status="resolved")

        # Check it's resolved
        defects = db.get_open_defects()
        assert len(defects) == 0
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_database_landmine_operations():
    """Test landmine create and retrieval."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        db = Database(db_path)
        db.initialize()

        # Create a landmine
        landmine_id = db.create_landmine(
            summary="Test gotcha",
            cause="Root cause",
            impact="High impact",
            remediation="Fix it",
            tags="testing",
        )

        assert landmine_id is not None
        assert landmine_id > 0

        # Get landmines
        landmines = db.get_landmines(limit=10)
        assert len(landmines) > 0
        assert landmines[0]["summary"] == "Test gotcha"
        assert landmines[0]["tags"] == "testing"
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_database_logging():
    """Test agent logging with trace IDs."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        db = Database(db_path)
        db.initialize()

        # Generate trace ID
        trace_id = db.generate_trace_id()
        assert trace_id is not None
        assert len(trace_id) == 36  # UUID format

        # Log an action
        log_id = db.log_action("TestAgent", "test_action", "Testing", trace_id=trace_id)
        assert log_id is not None
        assert log_id > 0

        # End action
        db.end_action(log_id)

        # Get recent actions
        actions = db.get_recent_actions(limit=10)
        assert len(actions) > 0
        assert actions[0]["agent"] == "TestAgent"
        assert actions[0]["action"] == "test_action"
        assert actions[0]["trace_id"] == trace_id
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_database_testing_status():
    """Test testing status tracking."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        db = Database(db_path)
        db.initialize()

        # Record test run
        testing_id = db.record_test_run("unit_tests", "passed", "All tests passed")
        assert testing_id is not None
        assert testing_id > 0

        # Update test status
        db.update_test_status(testing_id, "active", "passed")

        # Verify update
        test = db.execute_one("SELECT * FROM testing WHERE id = ?", (testing_id,))
        assert test is not None
        assert test["area"] == "unit_tests"
        assert test["last_run_status"] == "passed"
    finally:
        Path(db_path).unlink(missing_ok=True)


def test_database_config_operations():
    """Test configuration management."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        db = Database(db_path)
        db.initialize()

        # Set config
        db.set_config("test_key", "test_value", scope="global", source="test")

        # Get config
        configs = db.get_config("global")
        assert len(configs) > 0

        # Find our config
        test_config = None
        for config in configs:
            if config["name"] == "test_key":
                test_config = config
                break

        assert test_config is not None
        assert test_config["value"] == "test_value"
    finally:
        Path(db_path).unlink(missing_ok=True)
