"""Clide Dashboard - Web interface for viewing project memory bank."""

import os
import sqlite3

from flask import Flask, render_template_string

DB = os.getenv("CLIDE_DB", "memory_bank.db")
app = Flask(__name__)

T = """
<!doctype html><title>Clide Dashboard</title>
<h1>Clide Dashboard</h1>
<p>DB: {{db}}</p>

<h2>Open Work</h2>
<table border=1 cellpadding=6>
<tr><th>Kind</th><th>ID</th><th>Title</th><th>Status</th><th>Priority</th><th>Assignee</th><th>Updated</th></tr>
{% for r in open_work %}
<tr>
<td>{{r['kind']}}</td><td>{{r['id']}}</td><td>{{r['title']}}</td><td>{{r['status']}}</td><td>{{r['priority']}}</td><td>{{r['assignee']}}</td><td>{{r['updated_at']}}</td>
</tr>
{% endfor %}
</table>

<h2>Critical Defects</h2>
<ul>
{% for d in crit %}
<li>#{{d['id']}} {{d['title']}} — {{d['status']}}</li>
{% endfor %}
</ul>

<h2>Landmines (recent)</h2>
<ul>
{% for l in land %}
<li>#{{l['id']}} {{l['summary']}} <em>({{l['solution_verification']}})</em></li>
{% endfor %}
</ul>
"""


def q(sql, args=()):
    """Execute SQL query and return results as Row objects."""
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        return c.execute(sql, args).fetchall()


@app.route("/")
def home():
    """Render dashboard homepage with open work, critical defects, and landmines."""
    open_work = q("SELECT * FROM v_open_work LIMIT 50")
    crit = q(
        "SELECT id,title,status FROM defects WHERE status IN ('open','in_progress','blocked') AND severity='critical' ORDER BY id DESC LIMIT 20"
    )
    land = q(
        "SELECT id,summary,solution_verification FROM landmines ORDER BY updated_at DESC LIMIT 20"
    )
    return render_template_string(T, db=DB, open_work=open_work, crit=crit, land=land)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
