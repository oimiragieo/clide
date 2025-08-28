# /clide-report <milestones|landmines|defects|stories>

## Behavior
Render a markdown table for the selected type and write to `reports/<type>-YYYY-MM-DD.md`.

### Example (landmines)
```sql
SELECT id, summary, tags, solution_verification, remediation, avoidance_rules, updated_at
FROM landmines
ORDER BY updated_at DESC;
```
