"""Boot command implementation."""

from ..db import db
from ..utils import (
    format_priority,
    print_error,
    print_info,
    print_success,
    print_table,
    truncate,
)


def boot_command(summary: bool = False) -> None:
    """Boot Clide context: load landmines, open work, and deployment info."""
    print_success("Booting Clide context...")

    trace_id = db.generate_trace_id()
    log_id = db.log_action("Clide", "boot", "Loading context", trace_id=trace_id)

    try:
        # Get open work
        open_work = db.get_open_work(limit=20)
        print_info(f"Found {len(open_work)} open work items")

        if not summary and open_work:
            # Format for display
            display_work = []
            for item in open_work:
                display_work.append(
                    {
                        "Kind": item["kind"].title(),
                        "ID": f"#{item['id']}",
                        "Title": truncate(item["title"], 40),
                        "Status": item["status"],
                        "Priority": format_priority(item["priority"]),
                    }
                )
            print_table(
                display_work,
                title="Open Work",
                columns=["Kind", "ID", "Title", "Status", "Priority"],
            )

        # Get landmines
        landmines = db.get_landmines(limit=10)
        print_info(f"Found {len(landmines)} recent landmines")

        if not summary and landmines:
            display_landmines = []
            for item in landmines:
                display_landmines.append(
                    {
                        "ID": f"#{item['id']}",
                        "Summary": truncate(item["summary"], 50),
                        "Tags": item.get("tags", ""),
                    }
                )
            print_table(
                display_landmines, title="Recent Landmines", columns=["ID", "Summary", "Tags"]
            )

        # Get critical defects
        defects = db.get_open_defects()
        critical_defects = [d for d in defects if d["severity"] == "critical"]

        if critical_defects:
            print_info(f"⚠️  {len(critical_defects)} CRITICAL defects require attention!")
            if not summary:
                display_defects = []
                for item in critical_defects:
                    display_defects.append(
                        {
                            "ID": f"#{item['id']}",
                            "Title": truncate(item["title"], 50),
                            "Status": item["status"],
                        }
                    )
                print_table(
                    display_defects, title="Critical Defects", columns=["ID", "Title", "Status"]
                )

        # Get recent configuration
        configs = db.get_config()
        if configs and not summary:
            print_info(f"Configuration: {len(configs)} settings loaded")

        print_success("Context loaded successfully")
        print_info(f"Session trace ID: {trace_id}")

        db.end_action(log_id)

    except Exception as e:
        print_error(f"Failed to boot context: {e}")
        raise
