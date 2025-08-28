# sqlite3 Cheatsheet

# List tables
sqlite3 memory_bank.db "SELECT name FROM sqlite_schema WHERE type='table'"

# Pretty output
sqlite3 -column -header memory_bank.db "SELECT * FROM stories LIMIT 5"

# Import CSV
sqlite3 memory_bank.db <<'SQL'
.mode csv
.import stories.csv stories
SQL
