# Clide v1.1 — Project Memory Starter Kit

Turn any repo into a self-documenting, self-improving project with a tiny SQLite memory bank + markdown slash-commands.

## What's inside

- `memory_bank.schema.sql` – base schema (v1.0)
- `migrations/2025-08-28-v1_1.sql` – upgrade to v1.1 (relations, triggers, verifications, richer logging)
- `init_db.sh`, `init_db.ps1` – create `memory_bank.db`
- `CLAUDE.md` – seed primer for your agent (Clide)
- `slash-commands/` – `/clide-save`, `/clide-boot`, `/clide-fix`, `/clide-status`, `/clide-report`
- `hooks/` – portable git hook scripts + installer
- `.github/workflows/` – CI integration and weekly lessons
- `dash.py` – lightweight Flask dashboard
- `speak.sh` – optional macOS audible greeting
- `tools/sqlite-cheatsheet.md` – quick reference
- `agents_log.md` – starter log
- `LICENSE` – MIT

## Quickstart

```bash
# 1) Create DB
chmod +x ./init_db.sh && ./init_db.sh

# 2) (Optional) install portable git hooks
chmod +x hooks/install-hooks.sh && hooks/install-hooks.sh

# 3) Run dashboard (Flask)
python3 dash.py  # http://127.0.0.1:5000

# 4) In your agent (Claude/Cursor/etc.)
/init
/clide-boot
/clide-save
```

## Notes

- SQLite is in WAL mode for safety with concurrent reads.
- All migrations are idempotent (safe to re-run).
- CI jobs are optional; they gracefully no-op if `memory_bank.db` is absent.
- Hooks are portable—copy from `hooks/` to `.git/hooks/` using `hooks/install-hooks.sh`.
