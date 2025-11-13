"""Config command implementation."""

from typing import Optional

from ..db import db
from ..utils import print_error, print_info, print_success, print_table


def config_command(
    key: str,
    value: Optional[str] = None,
    scope: str = "global",
    delete: bool = False,
    list_all: bool = False,
) -> None:
    """Manage Clide configuration."""
    if list_all:
        # List all configuration
        configs = db.execute("SELECT * FROM configuration ORDER BY scope, name")
        if not configs:
            print_info("No configuration found")
            return

        display_configs = []
        for c in configs:
            display_configs.append(
                {
                    "Scope": c["scope"],
                    "Name": c["name"],
                    "Value": c["value"][:50] if len(c["value"]) > 50 else c["value"],
                    "Source": c["source"],
                }
            )
        print_table(
            display_configs,
            title="Configuration",
            columns=["Scope", "Name", "Value", "Source"],
        )
        return

    if delete:
        # Delete configuration
        db.execute("DELETE FROM configuration WHERE scope = ? AND name = ?", (scope, key))
        print_success(f"Deleted configuration '{key}' from scope '{scope}'")
        return

    if value is None:
        # Get specific configuration
        result = db.execute_one(
            "SELECT * FROM configuration WHERE scope = ? AND name = ?", (scope, key)
        )
        if result:
            print_info(f"{result['scope']}.{result['name']} = {result['value']}")
            if result["notes"]:
                print_info(f"Notes: {result['notes']}")
        else:
            print_error(f"Configuration '{key}' not found in scope '{scope}'")
        return

    # Set configuration
    db.set_config(key, value, scope=scope, source="user")
    print_success(f"Set {scope}.{key} = {value}")
