"""Main CLI entry point for Clide."""

import sys

import click
from rich.console import Console

from . import __version__
from .config import config
from .utils import print_error, print_info

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="clide")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--db", default=None, help="Path to database file")
@click.pass_context
def cli(ctx, verbose, db):
    """Clide - World-class AI agent CLI for project memory management.

    Transform your repository into a self-documenting, self-improving project
    with persistent memory, automated insights, and AI-powered assistance.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    if db:
        config.db_path = db
    config.verbose = verbose


@cli.command()
@click.option("--force", is_flag=True, help="Force re-initialization")
@click.pass_context
def init(ctx, force):
    """Initialize Clide memory bank database."""
    from .commands.init import init_command

    init_command(force)


@cli.command()
@click.option("--summary", is_flag=True, help="Show brief summary only")
@click.pass_context
def boot(ctx, summary):
    """Boot Clide context: load landmines, open work, and deployment info."""
    from .commands.boot import boot_command

    boot_command(summary)


@cli.command()
@click.option("--message", "-m", help="Save message/description")
@click.option("--trace-id", help="Trace ID for session grouping")
@click.pass_context
def save(ctx, message, trace_id):
    """Save current session facts to database."""
    from .commands.save import save_command

    save_command(message, trace_id)


@cli.command()
@click.option("--detailed", is_flag=True, help="Show detailed status")
@click.pass_context
def status(ctx, detailed):
    """Show quick snapshot of project health."""
    from .commands.status import status_command

    status_command(detailed)


@cli.command()
@click.argument("defect_id", type=int, required=False)
@click.option("--auto", is_flag=True, help="Automatically fix defect (requires AI)")
@click.pass_context
def fix(ctx, defect_id, auto):
    """Plan, patch, and prove a fix for a defect.

    If DEFECT_ID is provided, fix that specific defect.
    Otherwise, show all open defects.
    """
    from .commands.fix import fix_command

    fix_command(defect_id, auto)


@cli.command()
@click.argument(
    "table",
    type=click.Choice(
        ["milestones", "landmines", "defects", "stories", "config", "testing", "deployment"]
    ),
)
@click.option("--output", "-o", help="Output file path (default: stdout)")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["markdown", "json", "csv"]),
    default="markdown",
    help="Output format",
)
@click.pass_context
def report(ctx, table, output, fmt):
    """Generate markdown report for specified table."""
    from .commands.report import report_command

    report_command(table, output, fmt)


@cli.command()
@click.option("--host", default="127.0.0.1", help="Dashboard host")
@click.option("--port", default=5000, type=int, help="Dashboard port")
@click.option("--debug", is_flag=True, help="Run in debug mode")
@click.pass_context
def dashboard(ctx, host, port, debug):
    """Launch web dashboard for viewing memory bank."""
    from .commands.dashboard import dashboard_command

    dashboard_command(host, port, debug)


@cli.command()
@click.argument("key")
@click.argument("value", required=False)
@click.option("--scope", default="global", help="Configuration scope")
@click.option("--delete", is_flag=True, help="Delete configuration key")
@click.option("--list", "list_all", is_flag=True, help="List all configuration")
@click.pass_context
def config_cmd(ctx, key, value, scope, delete, list_all):
    """Manage Clide configuration.

    Examples:
        clide config --list
        clide config database.version
        clide config api.endpoint https://api.example.com
        clide config --delete old.key
    """
    from .commands.config import config_command

    config_command(key, value, scope, delete, list_all)


@cli.command()
@click.option("--output", "-o", help="Backup file path")
@click.pass_context
def backup(ctx, output):
    """Create a backup of the memory bank database."""
    from .commands.backup import backup_command

    backup_command(output)


@cli.command()
@click.argument("title")
@click.option("--description", "-d", help="Story description")
@click.option("--priority", "-p", type=int, default=3, help="Priority (1-5)")
@click.option("--assignee", "-a", help="Assignee name")
@click.option("--labels", "-l", help="Comma-separated labels")
@click.pass_context
def story(ctx, title, description, priority, assignee, labels):
    """Create a new story/work item."""
    from .commands.story import story_command

    story_command(title, description, priority, assignee, labels)


@cli.command()
@click.argument("title")
@click.option("--description", "-d", help="Defect description")
@click.option(
    "--severity",
    "-s",
    type=click.Choice(["critical", "major", "minor", "trivial"]),
    default="major",
    help="Defect severity",
)
@click.option("--story-id", type=int, help="Link to story ID")
@click.pass_context
def defect(ctx, title, description, severity, story_id):
    """Create a new defect/bug report."""
    from .commands.defect import defect_command

    defect_command(title, description, severity, story_id)


@cli.command()
@click.argument("summary")
@click.option("--cause", "-c", help="Root cause")
@click.option("--impact", "-i", help="Impact description")
@click.option("--remediation", "-r", help="How to fix")
@click.option("--tags", "-t", help="Comma-separated tags")
@click.pass_context
def landmine(ctx, summary, cause, impact, remediation, tags):
    """Record a gotcha/landmine for future reference."""
    from .commands.landmine import landmine_command

    landmine_command(summary, cause, impact, remediation, tags)


@cli.command()
@click.option("--limit", "-n", type=int, default=50, help="Number of entries to show")
@click.option("--agent", help="Filter by agent name")
@click.pass_context
def log(ctx, limit, agent):
    """Show recent agent activity log."""
    from .commands.log import log_command

    log_command(limit, agent)


def main():
    """Main entry point."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        print_info("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        if config.verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
