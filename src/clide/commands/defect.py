"""Defect command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_info, print_success


def defect_command(
    title: str,
    description: Optional[str] = None,
    severity: str = "major",
    story_id: Optional[int] = None,
) -> None:
    """Create a new defect/bug report."""
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
