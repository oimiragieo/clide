"""Story command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_info, print_success


def story_command(
    title: str,
    description: Optional[str] = None,
    priority: int = 3,
    assignee: Optional[str] = None,
    labels: Optional[str] = None,
) -> None:
    """Create a new story/work item."""
    story_id = db.create_story(
        title=title,
        description=description,
        priority=priority,
        assignee=assignee,
        labels=labels,
    )

    print_success(f"Created story #{story_id}: {title}")
    print_info(f"Priority: {priority}, Assignee: {assignee or 'unassigned'}")

    # Log creation
    db.log_action(
        "Clide",
        "create_story",
        f"Created story #{story_id}: {title}",
        trace_id=db.generate_trace_id(),
    )
