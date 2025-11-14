"""Status command implementation."""

from ..db import db
from ..utils import print_info, print_panel, print_success, print_table


def status_command(detailed: bool = False) -> None:
    """Show quick snapshot of project health."""
    print_success("Project Health Status")

    # Get counts
    stories = db.get_open_stories()
    defects = db.get_open_defects()
    landmines = db.get_landmines(limit=100)

    # Count by status
    story_todo = len([s for s in stories if s["status"] == "todo"])
    story_progress = len([s for s in stories if s["status"] == "in_progress"])
    story_blocked = len([s for s in stories if s["status"] == "blocked"])

    defect_open = len([d for d in defects if d["status"] == "open"])
    defect_progress = len([d for d in defects if d["status"] == "in_progress"])
    defect_blocked = len([d for d in defects if d["status"] == "blocked"])

    # Count by severity
    critical = len([d for d in defects if d["severity"] == "critical"])
    major = len([d for d in defects if d["severity"] == "major"])
    minor = len([d for d in defects if d["severity"] == "minor"])

    # Build summary
    summary = f"""
📊 **Work Items**: {len(stories)} total
   - TODO: {story_todo}
   - In Progress: {story_progress}
   - Blocked: {story_blocked}

🐛 **Defects**: {len(defects)} total
   - Open: {defect_open}
   - In Progress: {defect_progress}
   - Blocked: {defect_blocked}

⚠️  **By Severity**:
   - Critical: {critical}
   - Major: {major}
   - Minor: {minor}

💣 **Landmines**: {len(landmines)} recorded
"""

    print_panel(summary.strip(), title="Project Health", style="cyan")

    if detailed:
        print_info("\n📋 Top Priority Stories:")
        if stories:
            top_stories = sorted(stories, key=lambda x: (x["priority"], x["created_at"]))[:5]
            story_data = []
            for s in top_stories:
                story_data.append(
                    {
                        "ID": f"#{s['id']}",
                        "Title": s["title"][:50],
                        "Priority": s["priority"],
                        "Status": s["status"],
                    }
                )
            print_table(story_data, columns=["ID", "Title", "Priority", "Status"])
        else:
            print_info("  No open stories")

        print_info("\n🔥 Critical Defects:")
        critical_defects = [d for d in defects if d["severity"] == "critical"]
        if critical_defects:
            defect_data = []
            for d in critical_defects:
                defect_data.append(
                    {
                        "ID": f"#{d['id']}",
                        "Title": d["title"][:50],
                        "Status": d["status"],
                    }
                )
            print_table(defect_data, columns=["ID", "Title", "Status"])
        else:
            print_success("  No critical defects!")

    # Log status check
    db.log_action(
        "Clide",
        "status",
        f"Status check: {len(stories)} stories, {len(defects)} defects",
        trace_id=db.generate_trace_id(),
    )
