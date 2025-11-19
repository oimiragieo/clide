# Clide v1.1 — AI-Powered Project Memory Management CLI

Transform your repository into a **self-documenting, self-improving project** with persistent memory, automated insights, and AI-powered assistance.

Clide is a Python-based CLI tool that uses SQLite to maintain project context, track work, learn from past experiences, and help AI agents (and humans) stay productive.

---

## Features

- **14 CLI Commands** - Full-featured command-line interface
- **SQLite Memory Bank** - Persistent knowledge storage with WAL mode
- **Beautiful Terminal UI** - Rich formatting and color-coded output
- **Web Dashboard** - Optional Flask-based visual interface
- **Git Hooks** - Auto-save and test integration
- **GitHub Actions** - Automated CI/CD and weekly reports
- **AI Agent Integration** - SQL templates for AI workflows
- **Work Tracking** - Stories, defects, landmines, and testing
- **Report Generation** - Markdown, JSON, and CSV exports

---

## Quickstart

### 1. Install Dependencies (REQUIRED)

```bash
pip3 install -r requirements.txt
```

**Dependencies**: click, flask, rich, anthropic, python-dotenv, pytest, pytest-cov, black, ruff, pylint, mypy

### 2. Initialize Database

```bash
chmod +x ./init_db.sh && ./init_db.sh
```

**Windows**: Run `./init_db.ps1` instead

### 3. Start Using Clide

```bash
# Load project context
./clide boot

# Check project health
./clide status

# View all commands
./clide --help
```

### 4. (Optional) Install Git Hooks

```bash
chmod +x hooks/install-hooks.sh && hooks/install-hooks.sh
```

### 5. (Optional) Launch Web Dashboard

```bash
# Using CLI command
./clide dashboard

# OR using standalone script
python3 dash.py
```

Visit http://127.0.0.1:5000

---

## CLI Commands

### Initialization & Context
- `clide init` - Initialize memory bank database
- `clide boot` - Load context (landmines, open work, deployment, config)
- `clide save` - Save session checkpoint

### Project Health
- `clide status` - Show project health snapshot
- `clide log` - View agent activity log

### Work Management
- `clide story <title>` - Create work item/story
- `clide defect <title>` - Create defect/bug report
- `clide landmine <summary>` - Record gotcha/pitfall
- `clide fix [defect_id]` - Analyze and fix defects

### Reporting & Export
- `clide report <table>` - Generate reports (markdown, JSON, CSV)
- `clide dashboard` - Launch web UI

### Configuration & Maintenance
- `clide config <key> [value]` - Manage configuration
- `clide backup` - Backup database

---

## Usage Examples

### Track Your Work

```bash
# Create a feature story
./clide story "Add user authentication" --priority 1 --assignee alice

# Report a bug
./clide defect "Login button not working" --severity critical

# Document a gotcha
./clide landmine "API keys must be in .env file" --tags security
```

### Generate Reports

```bash
# Markdown report
./clide report defects -o reports/defects.md

# JSON export
./clide report stories --format json -o data.json

# CSV for analysis
./clide report landmines --format csv -o landmines.csv
```

### Daily Workflow

```bash
# Morning: load context
./clide boot

# During work: track discoveries
./clide landmine "Discovered: Redis timeout needs tuning" -t performance

# End of day: save progress
./clide save -m "End of day checkpoint"

# Backup
./clide backup -o backup.db
```

---

## What's Inside

### Core Files
- `src/clide/` - Python package (CLI, database, commands, utilities)
- `tests/` - Test suite (pytest)
- `memory_bank.schema.sql` - Base database schema (v1.0)
- `migrations/2025-08-28-v1_1.sql` - Schema upgrade to v1.1
- `init_db.sh` / `init_db.ps1` - Database initialization scripts
- `clide` - Executable wrapper
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Modern Python packaging configuration

### Documentation
- `CLAUDE.md` - Comprehensive AI agent primer
- `AUDIT_REPORT.md` - Detailed codebase audit (generated)
- `IMPROVEMENTS.md` - v1.1.0 changelog
- `README.md` - This file

### AI Agent Integration
- `slash-commands/` - SQL template documentation for AI agents
  - `/clide-boot` - Load full context
  - `/clide-save` - Save session data
  - `/clide-status` - Project health metrics
  - `/clide-fix` - Defect resolution workflow
  - `/clide-report` - Report generation

### Automation
- `hooks/` - Git hooks (pre-commit, pre-push) + installer
- `.github/workflows/` - GitHub Actions
  - `ci.yml` - Continuous integration (lint, test)
  - `lessons.yml` - Weekly lessons report

### Utilities
- `dash.py` - Standalone Flask dashboard
- `speak.sh` - macOS voice output (optional)
- `tools/sqlite-cheatsheet.md` - Quick SQLite reference
- `agents_log.md` - Activity log (manual)

---

## Database Schema

### Tables (11 total)
- **meta** - Schema version tracking
- **configuration** - Environment/config key-value storage
- **stories** - Work items/features
- **defects** - Bug tracking
- **landmines** - Gotchas/pitfalls documentation
- **testing** - Test procedures
- **deployment** - Deployment procedures by environment
- **milestones** - Achievement tracking
- **agents_log** - Activity logging with call stacks
- **story_defects** - M2M relationship (v1.1)
- **testing_defects** - M2M relationship (v1.1)

### Views (3 total)
- **v_open_work** - Combined open stories + defects
- **v_defects_with_stories** - Defects with linked stories
- **v_defects_with_tests** - Defects with linked tests

---

## Configuration

### Environment Variables

Create a `.env` file:

```bash
CLIDE_DB=memory_bank.db
CLIDE_DASHBOARD_HOST=127.0.0.1
CLIDE_DASHBOARD_PORT=5000
CLIDE_VERBOSE=false
ANTHROPIC_API_KEY=sk-...  # For future AI features
```

### CLI Flags

```bash
./clide --help               # Show help
./clide --version            # Show version
./clide --verbose status     # Verbose output
./clide --db custom.db boot  # Custom database path
```

---

## Git Hooks

### pre-commit Hook
- Auto-saves session to database
- Attempts `clide save` with SQL fallback
- Skips in CI environment

### pre-push Hook
- Runs pytest test suite
- Creates defect entry on test failure
- Logs results to database

Install hooks: `chmod +x hooks/install-hooks.sh && hooks/install-hooks.sh`

---

## CI/CD Integration

### GitHub Actions

#### ci.yml (Continuous Integration)
- **Triggers**: push, pull_request
- **Steps**: Install deps → Lint (ruff, black) → Test (pytest)
- **Logging**: Failures logged to defects table

#### lessons.yml (Weekly Reports)
- **Triggers**: Weekly (Mondays 13:00 UTC) + manual dispatch
- **Output**: Generates lessons report from landmines/defects
- **Action**: Auto-commits to reports/ folder
- **Tracking**: Creates milestone entries

---

## Development

### Adding a New Command

1. Create `src/clide/commands/mycommand.py`:
```python
from ..utils import print_success

def mycommand_command(arg):
    print_success(f"Executed with {arg}")
```

2. Register in `src/clide/cli.py`:
```python
@cli.command()
@click.argument("arg")
def mycommand(arg):
    from .commands.mycommand import mycommand_command
    mycommand_command(arg)
```

### Running Tests

```bash
pytest tests/ -v --cov=src/clide
```

### Linting & Formatting

```bash
ruff check src/
black --check src/
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'click'"

Install dependencies first:
```bash
pip3 install -r requirements.txt
```

### "Database is locked"

Check for stale connections:
```bash
lsof memory_bank.db  # Linux/macOS
```

### "Permission denied: ./clide"

Make executable:
```bash
chmod +x ./clide
```

### "Database not found"

Initialize first:
```bash
./init_db.sh
```

---

## Technical Details

- **Language**: Python 3.8+
- **CLI Framework**: Click 8.0+
- **Database**: SQLite3 with WAL mode (concurrent reads)
- **UI**: Rich library for terminal formatting
- **Web**: Flask 3.0+ for dashboard
- **Testing**: pytest with coverage
- **Linting**: ruff, black, pylint
- **Type Checking**: mypy (configured but optional)
- **Packaging**: Modern pyproject.toml

---

## Notes

- SQLite is in **WAL mode** for safety with concurrent reads
- All migrations are **idempotent** (safe to re-run)
- CI jobs gracefully no-op if `memory_bank.db` is absent
- Hooks are portable (install via `hooks/install-hooks.sh`)
- Dashboard has no authentication (use firewall for remote access)
- Slash commands in `slash-commands/` are **documentation templates**, not executable commands

---

## Resources

- **Full Documentation**: See `CLAUDE.md`
- **Audit Report**: See `AUDIT_REPORT.md`
- **Changelog**: See `IMPROVEMENTS.md`
- **SQLite Reference**: See `tools/sqlite-cheatsheet.md`

---

## License

MIT - See LICENSE file

---

## Version

**Current**: 1.1.0
**Schema**: 1.1
**Python**: 3.8+
**Last Updated**: 2025-11-18
