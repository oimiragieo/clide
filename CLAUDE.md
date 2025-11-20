# CLAUDE.md — Project Primer for Clide v1.1.0

> **Last Updated**: 2025-11-20 | **Schema**: 1.1 | **Python**: 3.8+

## What is Clide?

Clide is a **Python-based AI-powered project memory management CLI tool**. It provides persistent knowledge storage via SQLite, enabling AI agents and developers to maintain context, track work, and learn from past experiences.

**You are Clide**, the resident project co-pilot. You have two persistent responsibilities:
1. **Persist learning** into `memory_bank.db`
2. **Boot context** from `memory_bank.db` on demand

---

## Architecture Overview

### Technology Stack
- **Language**: Python 3.8+ (Click CLI framework)
- **Database**: SQLite3 with WAL mode
- **UI**: Rich library for beautiful terminal output
- **Web**: Flask dashboard (optional)
- **Packaging**: Modern Python packaging (pyproject.toml)

### Project Structure
```
clide/
├── src/clide/              # Main Python package
│   ├── cli.py              # Click-based CLI entry point
│   ├── db.py               # Database operations layer
│   ├── config.py           # Configuration management
│   ├── utils.py            # UI utilities (Rich formatting)
│   └── commands/           # 14 command implementations
├── tests/                  # Test suite (pytest)
├── slash-commands/         # AI agent SQL templates (NOT executable)
├── hooks/                  # Git hooks (pre-commit, pre-push)
├── migrations/             # Database migrations
├── .github/workflows/      # CI/CD (Python-based)
├── memory_bank.schema.sql  # Base database schema (v1.0)
├── init_db.sh/ps1          # Database initialization scripts
├── clide                   # Executable wrapper
└── requirements.txt        # Python dependencies
```

### Entry Points
1. **CLI Commands**: `./clide <command>` (14 commands available)
2. **Python Module**: `python3 -m clide <command>`
3. **Installed Binary**: `clide <command>` (after `pip install .`)

---

## Installation & Setup

### Step 1: Install Dependencies
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# OR install as editable package (for development)
pip3 install -e .

# Dependencies: click, flask, rich, anthropic, python-dotenv,
#               pytest, pytest-cov, black, ruff, pylint, mypy
```

### Step 2: Configure Environment (Optional)
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings (database path, API keys, etc.)
```

### Step 3: Initialize Database
```bash
# Create memory bank database (Linux/macOS)
chmod +x ./init_db.sh && ./init_db.sh

# On Windows
./init_db.ps1
```

### Step 4: Install Git Hooks (Optional)
```bash
chmod +x hooks/install-hooks.sh && hooks/install-hooks.sh
```

---

## Golden Rules

1. **Ask before destructive actions** - Never delete data without confirmation
2. **Log actions to database** - Use `db.log_action()` with trace_id/parent_id
3. **Elevate gotchas** - Record issues in `landmines` table immediately
4. **Use trace IDs** - Create fresh trace_id per session: `db.generate_trace_id()`
5. **Document learnings** - Update configuration, testing, deployment tables

---

## Core Capabilities

### 1. Database Operations
- **Tool**: Use `clide` CLI commands OR direct `sqlite3 memory_bank.db`
- **Schema**: 11 tables + 3 views (see Database Schema section)
- **Connection**: Managed via src/clide/db.py with context managers
- **Logging**: All actions logged to `agents_log` table

### 2. CLI Commands (14 Available)

#### Initialization & Context
- `clide init` - Initialize memory bank database
- `clide boot` - Load context (landmines, open work, deployment, config)
- `clide save` - Save session checkpoint

#### Project Health
- `clide status` - Show project health snapshot
- `clide log` - View agent activity log

#### Work Management
- `clide story <title>` - Create work item/story
- `clide defect <title>` - Create defect/bug report
- `clide defect --resolve <id> -r "resolution"` - Resolve existing defect
- `clide landmine <summary>` - Record gotcha/pitfall
- `clide fix [defect_id]` - Analyze and fix defects

#### Reporting & Export
- `clide report <table>` - Generate reports (markdown, JSON, CSV)
- `clide dashboard` - Launch web UI (http://127.0.0.1:5000)

#### Configuration & Maintenance
- `clide config <key> [value]` - Manage configuration
- `clide backup` - Backup database

### 3. File Operations
- Read/write markdown files as needed
- Update `agents_log.md` manually (auto-logging to file not yet implemented)
- Generate reports in reports/ directory

---

## Slash Commands (AI Agent Templates)

**IMPORTANT**: The files in `slash-commands/` are **SQL documentation templates** for AI agents, NOT executable CLI commands. They provide SQL queries and workflow patterns.

### Available Templates
- `/clide-boot` - SQL queries to load full context
- `/clide-save` - SQL upsert patterns for persistence
- `/clide-status` - SQL queries for health metrics
- `/clide-fix` - SQL workflow for defect resolution
- `/clide-report` - SQL queries for report generation

### Usage Pattern
AI agents should:
1. Read the slash command template
2. Extract SQL queries
3. Execute via `sqlite3 memory_bank.db` OR use equivalent `clide` CLI command

---

## Database Schema (v1.1)

### Core Tables

#### meta
- Tracks schema version

#### configuration
- Scope-based config storage (global, dev, prod, etc.)
- Keys: name, value, source, notes

#### stories
- Work items/features
- Fields: title, description, status, priority, labels, assignee, acceptance_criteria
- Statuses: todo, in_progress, blocked, completed

#### defects
- Bug tracking
- Fields: title, description, severity, status, story_id
- Severities: critical, major, minor, trivial
- Statuses: open, in_progress, blocked, resolved, closed

#### landmines
- Gotchas/pitfalls documentation
- Fields: summary, cause, impact, detection, remediation, avoidance_rules, tags, solution_verification

#### testing
- Test procedures
- Fields: area, preconditions, steps, expected, tools, status, owner, last_run_status, last_run_at

#### deployment
- Deployment procedures by environment
- Fields: environment, strategy, steps, scripts, last_deployed_at, verified_by

#### milestones
- Achievement tracking
- Fields: name, description, achieved_at, owner

#### agents_log
- Activity logging with call stacks
- Fields: agent, session_id, action, details, started_at, ended_at, parent_id, trace_id

### Relationship Tables (v1.1)
- **story_defects** - M2M: stories ↔ defects
- **testing_defects** - M2M: testing ↔ defects

### Views
- **v_open_work** - Combined open stories + defects
- **v_defects_with_stories** - Defects with linked stories
- **v_defects_with_tests** - Defects with linked tests

---

## Logging Workflow

### Create Session Trace
```python
from clide.db import db

trace_id = db.generate_trace_id()
log_id = db.log_action("Clide", "action_name", "details", trace_id=trace_id)

# ... perform action ...

db.end_action(log_id)
```

### Nested Actions
```python
parent_id = log_id  # Previous action
child_log_id = db.log_action("Clide", "sub_action", "details", trace_id=trace_id, parent_id=parent_id)
```

### Note
Currently, logging to `agents_log.md` is MANUAL. The database is the source of truth. To append to markdown:
```bash
echo "$(date): [Clide] Action performed" >> agents_log.md
```

---

## Configuration Management

### Environment Variables
- `CLIDE_DB` - Database path (default: memory_bank.db)
- `CLIDE_DASHBOARD_HOST` - Dashboard host (default: 127.0.0.1)
- `CLIDE_DASHBOARD_PORT` - Dashboard port (default: 5000)
- `CLIDE_VERBOSE` - Verbose output (default: false)

### .env File Support
Create `.env` file in project root:
```bash
CLIDE_DB=memory_bank.db
ANTHROPIC_API_KEY=sk-...
CLIDE_VERBOSE=true
```

### CLI Flags
- `--db <path>` - Override database path
- `--verbose` - Enable verbose output
- `--version` - Show version

---

## Workflow Patterns

### On Session Start
```bash
# 1. Load context
clide boot

# 2. Check project health
clide status

# 3. Review open work
clide report stories | head -20
clide report defects | head -20
```

### During Development
```bash
# Record discoveries
clide landmine "API keys must be in .env" -t security -r "Add .env.example"

# Track bugs
clide defect "Login fails on Safari" -s major -d "Details here"

# Create features
clide story "Add user dashboard" -p 1 -a alice
```

### Before Commit
```bash
# Save session (auto-triggered by pre-commit hook)
clide save -m "Session checkpoint"

# Backup database
clide backup
```

### Reporting
```bash
# Generate markdown reports
clide report landmines -o reports/landmines.md
clide report defects --format json -o reports/defects.json

# View dashboard
clide dashboard --port 8080
```

---

## Git Hooks Integration

### pre-commit Hook
- Auto-saves session to database
- Attempts `clide save` with SQL fallback
- Skips in CI environment

### pre-push Hook
- Runs pytest test suite
- Creates defect on test failure
- Logs to database

---

## CI/CD Integration

### GitHub Actions Workflows

#### ci.yml (Continuous Integration)
- Triggers: push, pull_request
- Steps: Install deps → Lint (ruff, black) → Test (pytest)
- Logs failures to defects table

#### lessons.yml (Weekly Reports)
- Triggers: Weekly (Mondays 13:00 UTC) + manual
- Generates lessons report from landmines/defects
- Auto-commits to reports/ folder
- Creates milestone entries

---

## Development Guidelines

### Adding New Commands
1. Create `src/clide/commands/mycommand.py`
2. Implement `mycommand_command()` function
3. Add to `src/clide/cli.py`:
   ```python
   @cli.command()
   def mycommand():
       from .commands.mycommand import mycommand_command
       mycommand_command()
   ```

### Database Operations
```python
from clide.db import db

# Query
rows = db.execute("SELECT * FROM stories WHERE status = ?", ("todo",))

# Insert
story_id = db.create_story(title="New story", priority=1)

# Update
db.execute("UPDATE stories SET status = ? WHERE id = ?", ("completed", story_id))
```

### UI Formatting
```python
from clide.utils import print_success, print_error, print_table

print_success("Operation completed")
print_error("Something went wrong")
print_table(data, title="Results", columns=["id", "title", "status"])
```

---

## Recent Improvements (v1.1)

### Implemented Features
1. ✅ **Defect resolution** - `clide defect --resolve <id>` command added
2. ✅ **Schema v1.1** - Added relationship tables (story_defects, testing_defects)
3. ✅ **Testing status tracking** - `last_run_status` and `last_run_at` fields added
4. ✅ **Improved documentation** - Comprehensive CLAUDE.md, README.md, AUDIT_REPORT.md
5. ✅ **Code quality** - Fixed all linting errors, added type hints
6. ✅ **dash.py documented** - Clarified as legacy standalone mode
7. ✅ **Environment configuration** - Added .env.example for easy setup

### Current Limitations
1. **AI API keys reserved for future use** - Configured but not actively used
2. **No authentication on dashboard** - Web UI is open access
3. **Voice output not integrated** - `speak.sh` exists but not used in commands

### Planned Features (Not Implemented)
- `clide fix --auto` - AI-powered auto-fix (placeholder)
- Voice output via `speak.sh` integration
- Dashboard authentication
- Multi-user support

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'click'"
```bash
# Install dependencies first
pip3 install -r requirements.txt
```

### "Database is locked"
```bash
# Check for stale connections
lsof memory_bank.db
# Kill processes if needed
```

### "Permission denied: ./clide"
```bash
chmod +x ./clide
```

### "Database not found"
```bash
# Initialize database first
./init_db.sh
```

---

## Quick Reference

### Essential Commands
```bash
# Setup
pip3 install -r requirements.txt && ./init_db.sh

# Daily workflow
clide boot                          # Load context
clide status                        # Check health
clide landmine "Discovery" -t tag   # Record learning
clide save -m "Session end"         # Save progress

# Reporting
clide report landmines              # Export learnings
clide dashboard                     # View web UI
```

### Database Direct Access
```bash
# Query
sqlite3 memory_bank.db "SELECT * FROM v_open_work LIMIT 10"

# Insert
sqlite3 memory_bank.db "INSERT INTO landmines(summary, tags) VALUES('Test', 'example')"

# Export
sqlite3 -markdown memory_bank.db "SELECT * FROM landmines" > report.md
```

---

## Additional Resources

- **Full Audit Report**: See `AUDIT_REPORT.md` for comprehensive codebase analysis
- **Improvements Log**: See `IMPROVEMENTS.md` for v1.1.0 changelog
- **SQLite Cheatsheet**: See `tools/sqlite-cheatsheet.md`
- **Schema**: See `memory_bank.schema.sql` and `migrations/2025-08-28-v1_1.sql`

---

## Version Information

| Component | Version | Notes |
|-----------|---------|-------|
| Clide CLI | 1.1.0 | Stable release |
| Database Schema | 1.1 | Current schema |
| Python Requirement | 3.8+ | Minimum version |
| Last Updated | 2025-11-20 | Documentation refresh |

**Dependencies**: See `requirements.txt` for full list
**Repository**: https://github.com/oimiragieo/clide
