# /clide-fix <defect_id>

## Goal
Plan → patch → prove for a specific defect.

## Load Context
- Target defect, related stories, related tests.
- Relevant landmines (matching tags) and configuration.

## Steps
1. Create a fix plan with acceptance checks.
2. (Optional) Spawn sub-agent `FixBot` with **stop condition**:
   “Linked tests passing locally; PR opened; defect → resolved; any related landmine → verified.”
3. Update testing.last_run_* after executing tests.
4. Log all nested actions with parent_id + trace_id.
5. On success, set `defect.status='resolved'` and add a resolution note.

## SQL Helpers
```sql
SELECT * FROM defects WHERE id=$defect_id;
SELECT s.* FROM stories s
JOIN story_defects sd ON sd.story_id=s.id WHERE sd.defect_id=$defect_id;
SELECT t.* FROM testing t
JOIN testing_defects td ON td.testing_id=t.id WHERE td.defect_id=$defect_id;
```
