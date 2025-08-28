# /clide-status

## Output
- Counts: open defects (by severity), stories by status, new landmines (7d)
- Top 5 blockers (blocked stories + open critical defects)
- Last deployments per environment
- Recent agent traces

## Queries
```sql
SELECT severity, COUNT(*) AS cnt FROM defects
WHERE status IN ('open','in_progress','blocked')
GROUP BY severity;

SELECT status, COUNT(*) AS cnt FROM stories GROUP BY status;

SELECT COUNT(*) AS new_landmines FROM landmines
WHERE created_at >= datetime('now','-7 days');

SELECT environment, MAX(last_deployed_at) AS last_deploy
FROM deployment GROUP BY environment;

SELECT trace_id, COUNT(*) AS actions, MIN(started_at) AS started, MAX(ended_at) AS ended
FROM agents_log WHERE trace_id IS NOT NULL
GROUP BY trace_id ORDER BY ended DESC LIMIT 5;
```
