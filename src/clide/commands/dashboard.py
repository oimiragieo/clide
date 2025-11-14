"""Dashboard command implementation."""

import sys

from ..config import config
from ..utils import print_error, print_info, print_success


def dashboard_command(host: str = "127.0.0.1", port: int = 5000, debug: bool = False) -> None:
    """Launch web dashboard for viewing memory bank."""
    if not config.db_exists:
        print_error("Database not found. Run 'clide init' first.")
        sys.exit(1)

    print_info(f"Starting dashboard at http://{host}:{port}")
    print_info("Press Ctrl+C to stop")

    try:
        # Import and run Flask app from dash.py
        import sqlite3

        from flask import Flask, render_template_string

        DB = config.db_path
        app = Flask(__name__)

        T = """
<!doctype html>
<html>
<head>
    <title>Clide Dashboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f4f4f4; font-weight: 600; }
        tr:hover { background-color: #f9f9f9; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.85em; }
        .critical { background: #ff4444; color: white; }
        .major { background: #ff8800; color: white; }
        .minor { background: #ffbb33; color: white; }
        .story { background: #0088cc; color: white; }
        .defect { background: #cc0000; color: white; }
    </style>
</head>
<body>
    <h1>🚀 Clide Dashboard</h1>
    <p><strong>Database:</strong> {{db}}</p>

    <h2>📋 Open Work</h2>
    <table>
        <tr>
            <th>Kind</th><th>ID</th><th>Title</th><th>Status</th>
            <th>Priority</th><th>Assignee</th><th>Updated</th>
        </tr>
        {% for r in open_work %}
        <tr>
            <td><span class="badge {{r['kind']}}">{{r['kind']}}</span></td>
            <td>#{{r['id']}}</td>
            <td>{{r['title']}}</td>
            <td>{{r['status']}}</td>
            <td>{{r['priority']}}</td>
            <td>{{r['assignee'] or '-'}}</td>
            <td>{{r['updated_at']}}</td>
        </tr>
        {% endfor %}
    </table>

    <h2>🐛 Critical Defects</h2>
    <ul>
    {% for d in crit %}
        <li><strong>#{{d['id']}}</strong> {{d['title']}} — <em>{{d['status']}}</em></li>
    {% endfor %}
    </ul>

    <h2>💣 Recent Landmines</h2>
    <ul>
    {% for l in land %}
        <li><strong>#{{l['id']}}</strong> {{l['summary']}}
        {% if l['solution_verification'] %}<em>({{l['solution_verification']}})</em>{% endif %}
        </li>
    {% endfor %}
    </ul>
</body>
</html>
        """

        def q(sql, args=()):
            with sqlite3.connect(DB) as c:
                c.row_factory = sqlite3.Row
                return c.execute(sql, args).fetchall()

        @app.route("/")
        def home():
            open_work = q("SELECT * FROM v_open_work LIMIT 50")
            crit = q(
                "SELECT id,title,status FROM defects "
                "WHERE status IN ('open','in_progress','blocked') "
                "AND severity='critical' ORDER BY id DESC LIMIT 20"
            )
            land = q(
                "SELECT id,summary,solution_verification FROM landmines "
                "ORDER BY updated_at DESC LIMIT 20"
            )
            return render_template_string(T, db=DB, open_work=open_work, crit=crit, land=land)

        print_success("Dashboard started successfully")
        app.run(host=host, port=port, debug=debug)

    except KeyboardInterrupt:
        print_info("\nDashboard stopped")
    except Exception as e:
        print_error(f"Failed to start dashboard: {e}")
        raise
