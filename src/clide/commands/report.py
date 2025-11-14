"""Report command implementation."""

import csv
import json
from typing import Optional

from ..db import db
from ..utils import print_error, print_info, print_success


def report_command(table: str, output: Optional[str] = None, fmt: str = "markdown") -> None:
    """Generate report for specified table."""
    # Query data based on table
    if table == "milestones":
        data = db.execute("SELECT * FROM milestones ORDER BY achieved_at DESC")
    elif table == "landmines":
        data = db.get_landmines(limit=1000)
    elif table == "defects":
        data = db.execute("SELECT * FROM defects ORDER BY created_at DESC")
    elif table == "stories":
        data = db.execute("SELECT * FROM stories ORDER BY created_at DESC")
    elif table == "config":
        data = db.get_config()
    elif table == "testing":
        data = db.execute("SELECT * FROM testing ORDER BY created_at DESC")
    elif table == "deployment":
        data = db.execute("SELECT * FROM deployment ORDER BY created_at DESC")
    else:
        print_error(f"Unknown table: {table}")
        return

    if not data:
        print_info(f"No data found for table '{table}'")
        return

    # Convert to dict
    data = [dict(row) for row in data]

    # Generate report based on format
    if fmt == "markdown":
        content = generate_markdown(table, data)
    elif fmt == "json":
        content = json.dumps(data, indent=2, default=str)
    elif fmt == "csv":
        content = generate_csv(data)
    else:
        print_error(f"Unknown format: {fmt}")
        return

    # Output
    if output:
        with open(output, "w") as f:
            f.write(content)
        print_success(f"Report written to {output}")
    else:
        from rich.console import Console

        console = Console()
        console.print(content)

    # Log report generation
    db.log_action(
        "Clide",
        "report",
        f"Generated {fmt} report for {table}",
        trace_id=db.generate_trace_id(),
    )


def generate_markdown(table: str, data: list) -> str:
    """Generate markdown report."""
    lines = [f"# {table.title()} Report", ""]
    lines.append(f"Generated: {db.execute_one('SELECT datetime(\"now\")')[0]}")
    lines.append(f"Total entries: {len(data)}")
    lines.append("")

    if not data:
        return "\n".join(lines)

    # Get columns
    columns = list(data[0].keys())

    # Table header
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

    # Table rows
    for row in data:
        values = [str(row.get(col, "")).replace("\n", " ").replace("|", r"\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def generate_csv(data: list) -> str:
    """Generate CSV report."""
    if not data:
        return ""

    import io

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
