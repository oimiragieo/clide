$DB="memory_bank.db"
$SCHEMA="memory_bank.schema.sql"
$MIGRATION="migrations/2025-08-28-v1_1.sql"

if (-not (Get-Command sqlite3 -ErrorAction SilentlyContinue)) {
  Write-Error "sqlite3 is required. On Windows, install via winget or scoop."
  exit 1
}

if (-not (Test-Path $SCHEMA)) {
  Write-Error "Missing $SCHEMA in current directory."
  exit 1
}

if (Test-Path $DB) { Remove-Item $DB -Force }
Write-Host "Initializing $DB from $SCHEMA ..."
sqlite3 $DB ".read $SCHEMA"

if (Test-Path $MIGRATION) {
  Write-Host "Applying migration $MIGRATION ..."
  sqlite3 $DB ".read $MIGRATION"
}

Write-Host "Tables:"
sqlite3 $DB ".tables"

Write-Host "Schema version:"
sqlite3 $DB "SELECT key, value FROM meta;"
