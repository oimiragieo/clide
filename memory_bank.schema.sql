PRAGMA journal_mode=WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;

/* ---------- Core meta ---------- */
CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at DATETIME DEFAULT (datetime('now'))
);

/* ---------- Configuration ---------- */
CREATE TABLE IF NOT EXISTS configuration (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scope TEXT NOT NULL DEFAULT 'global',
  name TEXT NOT NULL,
  value TEXT NOT NULL,
  source TEXT DEFAULT 'discovered',
  notes TEXT,
  created_at DATETIME DEFAULT (datetime('now')),
  updated_at DATETIME DEFAULT (datetime('now')),
  UNIQUE(scope, name)
);

/* ---------- Deployment ---------- */
CREATE TABLE IF NOT EXISTS deployment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  environment TEXT NOT NULL,
  strategy TEXT,
  steps TEXT NOT NULL,
  scripts TEXT,
  last_deployed_at DATETIME,
  verified_by TEXT,
  created_at DATETIME DEFAULT (datetime('now')),
  updated_at DATETIME DEFAULT (datetime('now'))
);

/* ---------- Testing ---------- */
CREATE TABLE IF NOT EXISTS testing (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  area TEXT NOT NULL,
  preconditions TEXT,
  steps TEXT NOT NULL,
  expected TEXT NOT NULL,
  tools TEXT,
  status TEXT DEFAULT 'unknown',
  owner TEXT,
  created_at DATETIME DEFAULT (datetime('now')),
  updated_at DATETIME DEFAULT (datetime('now'))
);

/* ---------- Stories ---------- */
CREATE TABLE IF NOT EXISTS stories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'todo',
  priority INTEGER DEFAULT 3,
  labels TEXT,
  assignee TEXT,
  acceptance_criteria TEXT,
  due_date DATE,
  created_at DATETIME DEFAULT (datetime('now')),
  updated_at DATETIME DEFAULT (datetime('now'))
);

/* ---------- Defects ---------- */
CREATE TABLE IF NOT EXISTS defects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  severity TEXT NOT NULL DEFAULT 'major',
  status TEXT NOT NULL DEFAULT 'open',
  story_id INTEGER REFERENCES stories(id) ON DELETE SET NULL,
  introduced_in TEXT,
  detected_by TEXT,
  created_at DATETIME DEFAULT (datetime('now')),
  resolved_at DATETIME,
  resolution TEXT
);

/* ---------- Milestones ---------- */
CREATE TABLE IF NOT EXISTS milestones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  achieved_at DATETIME DEFAULT (datetime('now')),
  owner TEXT
);

/* ---------- Landmines ---------- */
CREATE TABLE IF NOT EXISTS landmines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  summary TEXT NOT NULL,
  cause TEXT,
  impact TEXT,
  detection TEXT,
  remediation TEXT,
  avoidance_rules TEXT,
  tags TEXT,
  created_at DATETIME DEFAULT (datetime('now')),
  updated_at DATETIME DEFAULT (datetime('now'))
);

/* ---------- Agent activity log ---------- */
CREATE TABLE IF NOT EXISTS agents_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  agent TEXT NOT NULL,
  session_id TEXT,
  action TEXT NOT NULL,
  details TEXT,
  started_at DATETIME DEFAULT (datetime('now')),
  ended_at DATETIME
);

/* ---------- Helpful views ---------- */
CREATE VIEW IF NOT EXISTS v_open_work AS
SELECT 'story' AS kind, id, title, status, priority, labels, assignee, created_at, updated_at
FROM stories WHERE status IN ('todo','in_progress','blocked')
UNION ALL
SELECT 'defect' AS kind, id, title, status,
  CASE severity WHEN 'critical' THEN 1 WHEN 'major' THEN 2 WHEN 'minor' THEN 4 ELSE 3 END AS priority,
  NULL AS labels, NULL AS assignee, created_at, resolved_at
FROM defects WHERE status IN ('open','in_progress','blocked')
ORDER BY priority ASC, created_at ASC;

/* ---------- Indices ---------- */
CREATE INDEX IF NOT EXISTS idx_stories_status ON stories(status);
CREATE INDEX IF NOT EXISTS idx_defects_status ON defects(status);
CREATE INDEX IF NOT EXISTS idx_landmines_tags ON landmines(tags);
CREATE INDEX IF NOT EXISTS idx_config_scope_name ON configuration(scope, name);

/* ---------- Meta seed ---------- */
INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version','1');
