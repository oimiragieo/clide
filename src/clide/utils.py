"""Utility functions for Clide."""

from datetime import datetime
from typing import Any, Dict, List

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_success(message: str) -> None:
    """Print success message in green."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message in red."""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """Print info message in blue."""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_table(data: List[Dict[str, Any]], title: str = "", columns: List[str] = None) -> None:
    """Print data as a formatted table."""
    if not data:
        print_warning(f"No data to display for {title}")
        return

    # Use all keys from first row if columns not specified
    if columns is None:
        columns = list(data[0].keys())

    table = Table(title=title, show_header=True, header_style="bold magenta")

    for col in columns:
        table.add_column(col.replace("_", " ").title())

    for row in data:
        table.add_row(*[str(row.get(col, "")) for col in columns])

    console.print(table)


def print_panel(content: str, title: str = "", style: str = "cyan") -> None:
    """Print content in a panel."""
    console.print(Panel(content, title=title, border_style=style))


def print_markdown(content: str) -> None:
    """Print markdown content."""
    console.print(Markdown(content))


def format_datetime(dt: str) -> str:
    """Format datetime string for display."""
    if not dt:
        return ""
    try:
        parsed = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        return parsed.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return dt


def format_priority(priority: int) -> str:
    """Format priority with emoji."""
    if priority == 1:
        return "🔴 Critical"
    elif priority == 2:
        return "🟠 High"
    elif priority == 3:
        return "🟡 Medium"
    else:
        return "🟢 Low"


def format_status(status: str) -> str:
    """Format status with color."""
    status_map = {
        "todo": "[blue]TODO[/blue]",
        "in_progress": "[yellow]IN PROGRESS[/yellow]",
        "blocked": "[red]BLOCKED[/red]",
        "completed": "[green]COMPLETED[/green]",
        "open": "[red]OPEN[/red]",
        "resolved": "[green]RESOLVED[/green]",
        "closed": "[dim]CLOSED[/dim]",
    }
    return status_map.get(status.lower(), status)


def truncate(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis."""
    if not text:
        return ""
    return text[:max_length] + "..." if len(text) > max_length else text
