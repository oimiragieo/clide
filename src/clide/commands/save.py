"""Save command implementation."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from ..db import db
from ..utils import print_info, print_success, print_warning


def append_to_agents_log(message: str) -> bool:
    """Append entry to agents_log.md file.

    Args:
        message: The log message to append

    Returns:
        True if successful, False otherwise
    """
    try:
        log_file = Path("agents_log.md")

        # Read existing content to check structure
        if log_file.exists():
            content = log_file.read_text()

            # Get current date section header
            today = datetime.now().strftime("%Y-%m-%d")
            section_header = f"## {today}"

            # If today's section doesn't exist, add it
            if section_header not in content:
                # Append new date section
                with open(log_file, "a") as f:
                    f.write(f"\n{section_header}\n")

            # Append the log entry
            with open(log_file, "a") as f:
                f.write(f"- {message}\n")

            return True
        else:
            # Create new file if it doesn't exist
            with open(log_file, "w") as f:
                f.write("# Agents Log\n\n")
                f.write("> Append entries chronologically. Keep terse, atomic events.\n\n")
                f.write(f"## {datetime.now().strftime('%Y-%m-%d')}\n")
                f.write(f"- {message}\n")
            return True

    except Exception:
        return False


def save_command(message: Optional[str] = None, trace_id: Optional[str] = None) -> None:
    """Save current session facts to database."""
    if not trace_id:
        trace_id = db.generate_trace_id()

    details = message or "Session checkpoint"

    log_id = db.log_action("Clide", "save", details, trace_id=trace_id)

    print_success(f"Session saved (trace: {trace_id})")
    print_info(f"Log entry #{log_id}")

    # Get summary stats
    stories = db.get_open_stories()
    defects = db.get_open_defects()

    print_info(f"Current state: {len(stories)} open stories, {len(defects)} open defects")

    # Append to agents_log.md
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] [Clide] {details} (trace: {trace_id[:8]})"

    if append_to_agents_log(log_entry):
        print_info("Updated agents_log.md")
    else:
        print_warning("Could not update agents_log.md (continuing anyway)")

    db.end_action(log_id)
