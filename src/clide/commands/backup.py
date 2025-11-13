"""Backup command implementation."""

from datetime import datetime
from typing import Optional

from ..config import config
from ..utils import print_error, print_info, print_success


def backup_command(output: Optional[str] = None) -> None:
    """Create a backup of the memory bank database."""
    if not config.db_exists:
        print_error("Database not found. Nothing to backup.")
        return

    if output is None:
        # Generate default backup path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"memory_bank_backup_{timestamp}.db"

    print_info(f"Creating backup: {output}")

    try:
        from ..db import db

        success = db.backup(output)
        if success:
            print_success(f"Backup created successfully: {output}")
            db.log_action(
                "Clide", "backup", f"Created backup: {output}", trace_id=db.generate_trace_id()
            )
        else:
            print_error("Backup failed")
    except Exception as e:
        print_error(f"Backup failed: {e}")
        raise
