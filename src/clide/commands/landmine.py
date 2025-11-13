"""Landmine command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_info, print_success


def landmine_command(
    summary: str,
    cause: Optional[str] = None,
    impact: Optional[str] = None,
    remediation: Optional[str] = None,
    tags: Optional[str] = None,
) -> None:
    """Record a gotcha/landmine for future reference."""
    landmine_id = db.create_landmine(
        summary=summary,
        cause=cause,
        impact=impact,
        remediation=remediation,
        tags=tags,
    )

    print_success(f"Recorded landmine #{landmine_id}: {summary}")
    if tags:
        print_info(f"Tags: {tags}")

    # Log creation
    db.log_action(
        "Clide",
        "create_landmine",
        f"Recorded landmine #{landmine_id}: {summary}",
        trace_id=db.generate_trace_id(),
    )
