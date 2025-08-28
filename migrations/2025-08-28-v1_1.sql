-- v1.1: relationships, logging, verification, test status

PRAGMA foreign_keys = ON;

-- 1) Stories ↔ Defects: many-to-many
CREATE TABLE IF NOT EXISTS story_defects (
  story_id   INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
  defect_id  INTEGER NOT NULL REFERENCES defects(id) ON DELETE CASCADE,
  linked_at  DATETIME DEFAULT (datetime('now')),
  PRIMARY KEY (story_id, defect_id)
);

-- 2) Testing ↔ Defects: many-to-many
CREATE TABLE IF NOT EXISTS testing_defects (
  testing_id INTEGER NOT NULL REFERENCES testing(id) ON DELETE CASCADE,
  defect_id  INTEGER NOT NULL REFERENCES defects(id) ON DELETE CASCADE,
  evidence   TEXT,
  linked_at  DATETIME DEFAULT (datetime('now')),
  PRIMARY KEY (testing_id, defect_id)
);

-- 3) Testing last-run metadata
ALTER TABLE testing ADD COLUMN last_run_status TEXT DEFAULT NULL;
ALTER TABLE testing ADD COLUMN last_run_at     DATETIME DEFAULT NULL;

-- 4) Agents log call stacks
ALTER TABLE agents_log ADD COLUMN parent_id   INTEGER REFERENCES agents_log(id) ON DELETE SET NULL;
ALTER TABLE agents_log ADD COLUMN trace_id    TEXT;
CREATE INDEX IF NOT EXISTS idx_agents_log_parent ON agents_log(parent_id);
CREATE INDEX IF NOT EXISTS idx_agents_log_trace  ON agents_log(trace_id);

-- 5) Landmine fix verification
ALTER TABLE landmines ADD COLUMN solution_verification TEXT DEFAULT 'unverified';
CREATE INDEX IF NOT EXISTS idx_landmines_solution_verification ON landmines(solution_verification);

-- 6) Convenience views
CREATE VIEW IF NOT EXISTS v_defects_with_stories AS
SELECT d.*, GROUP_CONCAT(sd.story_id) AS story_ids
FROM defects d
LEFT JOIN story_defects sd ON sd.defect_id = d.id
GROUP BY d.id;

CREATE VIEW IF NOT EXISTS v_defects_with_tests AS
SELECT d.*, GROUP_CONCAT(td.testing_id) AS testing_ids
FROM defects d
LEFT JOIN testing_defects td ON td.defect_id = d.id
GROUP BY d.id;

-- 7) Triggers for timestamps and transitions
CREATE TRIGGER IF NOT EXISTS trg_stories_touch
AFTER UPDATE ON stories
BEGIN
  UPDATE stories SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_testing_touch
AFTER UPDATE ON testing
BEGIN
  UPDATE testing SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_deployment_touch
AFTER UPDATE ON deployment
BEGIN
  UPDATE deployment SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_defects_resolve
AFTER UPDATE OF status ON defects
WHEN NEW.status IN ('resolved','closed') AND (NEW.resolved_at IS NULL)
BEGIN
  UPDATE defects SET resolved_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_landmines_verified_milestone
AFTER UPDATE OF solution_verification ON landmines
WHEN NEW.solution_verification = 'verified'
BEGIN
  INSERT INTO milestones(name, description, owner)
  VALUES(
    'Verified fix: Landmine #' || NEW.id,
    COALESCE(NEW.summary,'(no summary)'),
    'Clide'
  );
END;

-- 8) Meta bump
INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version','1.1');
