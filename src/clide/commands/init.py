"""Initialize command implementation."""

from pathlib import Path

from ..config import config
from ..db import db
from ..utils import print_error, print_info, print_success


def init_command(force: bool = False) -> None:
    """Initialize Clide memory bank database."""
    db_path = Path(config.db_path)

    if db_path.exists() and not force:
        print_error(f"Database already exists at {config.db_path}")
        print_info("Use --force to re-initialize (this will destroy existing data)")
        return

    if force and db_path.exists():
        print_info(f"Removing existing database at {config.db_path}")
        db_path.unlink()

    print_info(f"Initializing database at {config.db_path}")

    try:
        success = db.initialize()
        if success:
            print_success("Database initialized successfully")
            print_info("Run 'clide boot' to load context")
            print_info("Run 'clide dashboard' to launch web UI")

            # Log initialization
            db.log_action("Clide", "init", "Database initialized", trace_id=db.generate_trace_id())
        else:
            print_error("Failed to initialize database (schema file not found)")
    except Exception as e:
        print_error(f"Failed to initialize database: {e}")
        raise
