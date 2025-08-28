#!/usr/bin/env bash
set -euo pipefail

DB="memory_bank.db"
SCHEMA="memory_bank.schema.sql"
MIGRATION="migrations/2025-08-28-v1_1.sql"

if ! command -v sqlite3 >/dev/null 2>&1; then
  echo "sqlite3 is required. On macOS: brew install sqlite3"
  exit 1
fi

if [ ! -f "$SCHEMA" ]; then
  echo "Missing $SCHEMA in current directory."
  exit 1
fi

echo "Initializing $DB from $SCHEMA ..."
rm -f "$DB"
sqlite3 "$DB" < "$SCHEMA"

if [ -f "$MIGRATION" ]; then
  echo "Applying migration $MIGRATION ..."
  sqlite3 "$DB" < "$MIGRATION"
fi

echo "Done. Created $DB"

echo "Tables:"
sqlite3 "$DB" ".tables"

echo "Schema version:"
sqlite3 "$DB" "SELECT key, value FROM meta;"
