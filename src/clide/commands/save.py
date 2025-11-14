"""Save command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_info, print_success


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

    db.end_action(log_id)
