"""Log command implementation."""

from typing import Optional

from ..db import db
from ..utils import format_datetime, print_info, print_table, truncate


def log_command(limit: int = 50, agent: Optional[str] = None) -> None:
    """Show recent agent activity log."""
    if agent:
        logs = db.execute(
            """
            SELECT id, agent, action, details, trace_id, started_at, ended_at
            FROM agents_log
            WHERE agent = ?
            ORDER BY started_at DESC
            LIMIT ?
            """,
            (agent, limit),
        )
    else:
        logs = db.get_recent_actions(limit)

    if not logs:
        print_info("No log entries found")
        return

    display_logs = []
    for log in logs:
        display_logs.append(
            {
                "ID": f"#{log['id']}",
                "Agent": log["agent"],
                "Action": log["action"],
                "Details": truncate(log.get("details", ""), 40),
                "Started": format_datetime(log["started_at"]),
            }
        )

    print_table(
        display_logs,
        title=f"Agent Activity Log (last {len(logs)})",
        columns=["ID", "Agent", "Action", "Details", "Started"],
    )
