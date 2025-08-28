# /clide-boot

## Purpose
Boot the project’s working memory from `memory_bank.db` into a single tactical brief.

## Queries
### Landmines (Top 10)
```sql
SELECT id, summary, tags, remediation, avoidance_rules, solution_verification
FROM landmines
ORDER BY updated_at DESC
LIMIT 10;
```

### Open Work (Stories & Defects)
```sql
SELECT * FROM v_open_work LIMIT 50;
```

### Deployment (by environment)
```sql
SELECT environment, strategy, steps, scripts, last_deployed_at
FROM deployment
ORDER BY environment;
```

### Configuration (interesting keys)
```sql
SELECT scope, name, value
FROM configuration
WHERE name IN ('NODE_VERSION','API_BASE_URL','DB_URL','REDIS_URL','AUTH_PROVIDER')
ORDER BY scope, name;
```

## Sections
1. **Greetings & Context Size** (optionally `say` on macOS)
2. **Do NOT do this (Landmines)** — read Top 3 aloud on macOS
3. **Top Priorities (Stories/Defects)**
4. **Deploy Playbook by Environment**
5. **Config Snapshot**
6. **Proposed Next Steps (3–5 bullets)**
7. **Append to agents_log.md**
