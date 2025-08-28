# /clide-save

## Purpose
Persist the current session’s facts into `memory_bank.db`.

## Behavior
1. Summarize the session into:
   - Config facts
   - Testing additions/updates (+ last_run_* if tests executed)
   - Deployment changes
   - New/updated stories
   - New/updated defects
   - New landmines (if any)
   - Agent activity log entries (with trace_id/parent_id)

2. Execute upserts with `sqlite3`.

### Upsert Examples

**configuration**
```sql
INSERT INTO configuration(scope, name, value, source, notes)
VALUES ($scope, $name, $value, $source, $notes)
ON CONFLICT(scope, name) DO UPDATE SET
  value=excluded.value,
  source=COALESCE(excluded.source, configuration.source),
  notes=CASE
    WHEN configuration.notes IS NULL OR configuration.notes=''
    THEN excluded.notes
    ELSE configuration.notes || CHAR(10) || excluded.notes
  END,
  updated_at=datetime('now');
```

**stories**
```sql
INSERT INTO stories(title, description, status, priority, labels, assignee, acceptance_criteria, due_date)
VALUES ($title,$description,$status,$priority,$labels,$assignee,$ac,$due_date);
```

**defects**
```sql
INSERT INTO defects(title, description, severity, status, introduced_in, detected_by)
VALUES ($title, $description, $severity, $status, $introduced_in, $detected_by);
```

**testing**
```sql
INSERT INTO testing(area, preconditions, steps, expected, tools, status, owner)
VALUES ($area,$pre,$steps,$expected,$tools,$status,$owner);
```

**link a test to a defect**
```sql
INSERT OR IGNORE INTO testing_defects(testing_id, defect_id, evidence)
VALUES ($testing_id, $defect_id, $evidence);
```

**log an agent action**
```sql
INSERT INTO agents_log(agent, session_id, action, details, started_at, ended_at, parent_id, trace_id)
VALUES ($agent,$session,$action,$details,$started,$ended,$parent,$trace);
```

## Output
- Print a concise “What I saved” checklist.
- Append to `agents_log.md` with timestamped actions.
