"""Fix command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_error, print_info, print_success, print_table, print_warning, truncate


def fix_command(defect_id: Optional[int] = None, auto: bool = False) -> None:
    """Plan, patch, and prove a fix for a defect."""
    if defect_id is None:
        # Show all open defects
        defects = db.get_open_defects()
        if not defects:
            print_success("No open defects! 🎉")
            return

        print_info(f"Found {len(defects)} open defects:")
        display_defects = []
        for d in defects:
            display_defects.append(
                {
                    "ID": f"#{d['id']}",
                    "Title": truncate(d["title"], 50),
                    "Severity": d["severity"],
                    "Status": d["status"],
                }
            )
        print_table(
            display_defects, title="Open Defects", columns=["ID", "Title", "Severity", "Status"]
        )
        print_info("\nRun 'clide fix <ID>' to fix a specific defect")
        return

    # Get specific defect
    defect = db.execute_one("SELECT * FROM defects WHERE id = ?", (defect_id,))
    if not defect:
        print_error(f"Defect #{defect_id} not found")
        return

    print_info(f"Analyzing defect #{defect_id}: {defect['title']}")
    print_info(f"Severity: {defect['severity']}")
    print_info(f"Status: {defect['status']}")

    if defect["description"]:
        print_info(f"Description: {defect['description']}")

    if auto:
        print_warning("⚠️  Auto-fix mode requires AI integration")
        print_info("AI-powered auto-fix is coming soon!")
        print_info("For now, please fix manually and use 'clide defect' to update status")
    else:
        print_info("\n📋 Suggested fix workflow:")
        print_info("1. Investigate the root cause")
        print_info("2. Implement the fix in your code")
        print_info("3. Test the fix thoroughly")
        print_info("4. Mark as resolved: clide defect --resolve #{defect_id}")

    # Log the fix attempt
    db.log_action(
        "Clide",
        "fix",
        f"Analyzed defect #{defect_id}",
        trace_id=db.generate_trace_id(),
    )
