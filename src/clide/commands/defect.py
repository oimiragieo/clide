"""Defect command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_error, print_info, print_success


def defect_command(
    title: str,
    description: Optional[str] = None,
    severity: str = "major",
    story_id: Optional[int] = None,
    resolve_id: Optional[int] = None,
    resolution: Optional[str] = None,
) -> None:
    """Create a new defect/bug report or resolve an existing one."""
    # Resolution mode
    if resolve_id is not None:
        # Get the defect
        defect = db.execute_one("SELECT * FROM defects WHERE id = ?", (resolve_id,))

        if not defect:
            print_error(f"Defect #{resolve_id} not found")
            return

        if defect["status"] in ("resolved", "closed"):
            print_error(f"Defect #{resolve_id} is already {defect['status']}")
            return

        # Resolve the defect
        resolution_text = resolution or title or "Resolved"
        db.resolve_defect(resolve_id, resolution_text, status="resolved")

        print_success(f"Resolved defect #{resolve_id}: {defect['title']}")
        print_info(f"Resolution: {resolution_text}")

        # Log resolution
        db.log_action(
            "Clide",
            "resolve_defect",
            f"Resolved defect #{resolve_id}: {defect['title']}",
            trace_id=db.generate_trace_id(),
        )

        return

    # Creation mode (default)
    defect_id = db.create_defect(
        title=title,
        description=description,
        severity=severity,
        detected_by="user",
        story_id=story_id,
    )

    print_success(f"Created defect #{defect_id}: {title}")
    print_info(f"Severity: {severity}")
    if story_id:
        print_info(f"Linked to story #{story_id}")

    # Log creation
    db.log_action(
        "Clide",
        "create_defect",
        f"Created defect #{defect_id}: {title}",
        trace_id=db.generate_trace_id(),
    )
