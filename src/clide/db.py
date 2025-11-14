"""Database operations for Clide."""

import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .config import config


class Database:
    """Database manager for Clide memory bank."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database manager."""
        self.db_path = db_path or config.db_path

    @contextmanager
    def connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 5000")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute(self, query: str, params: Union[tuple, dict] = ()) -> List[sqlite3.Row]:
        """Execute query and return results."""
        with self.connection() as conn:
            return conn.execute(query, params).fetchall()

    def execute_one(self, query: str, params: Union[tuple, dict] = ()) -> Optional[sqlite3.Row]:
        """Execute query and return first result."""
        with self.connection() as conn:
            result = conn.execute(query, params).fetchone()
            return result

    def execute_script(self, script: str) -> None:
        """Execute SQL script."""
        with self.connection() as conn:
            conn.executescript(script)

    def initialize(self) -> bool:
        """Initialize database from schema files."""
        schema_path = Path(__file__).parent.parent.parent / "memory_bank.schema.sql"
        migration_path = Path(__file__).parent.parent.parent / "migrations" / "2025-08-28-v1_1.sql"

        if not schema_path.exists():
            return False

        # Create database
        with open(schema_path) as f:
            self.execute_script(f.read())

        # Apply migrations
        if migration_path.exists():
            with open(migration_path) as f:
                self.execute_script(f.read())

        return True

    # ========== Agent Log Operations ==========

    def log_action(
        self,
        agent: str,
        action: str,
        details: Optional[str] = None,
        trace_id: Optional[str] = None,
        parent_id: Optional[int] = None,
    ) -> int:
        """Log an agent action."""
        query = """
            INSERT INTO agents_log (agent, action, details, trace_id, parent_id)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.connection() as conn:
            cursor = conn.execute(query, (agent, action, details, trace_id, parent_id))
            return cursor.lastrowid

    def end_action(self, log_id: int) -> None:
        """Mark action as ended."""
        query = "UPDATE agents_log SET ended_at = datetime('now') WHERE id = ?"
        self.execute(query, (log_id,))

    def get_recent_actions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent agent actions."""
        query = """
            SELECT id, agent, action, details, trace_id, parent_id,
                   started_at, ended_at
            FROM agents_log
            ORDER BY started_at DESC
            LIMIT ?
        """
        rows = self.execute(query, (limit,))
        return [dict(row) for row in rows]

    # ========== Configuration Operations ==========

    def get_config(self, scope: str = "global") -> List[Dict[str, Any]]:
        """Get configuration for scope."""
        query = "SELECT * FROM configuration WHERE scope = ? ORDER BY name"
        rows = self.execute(query, (scope,))
        return [dict(row) for row in rows]

    def set_config(
        self,
        name: str,
        value: str,
        scope: str = "global",
        source: str = "user",
        notes: Optional[str] = None,
    ) -> None:
        """Set configuration value."""
        query = """
            INSERT INTO configuration (scope, name, value, source, notes)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(scope, name) DO UPDATE SET
                value = excluded.value,
                source = excluded.source,
                notes = excluded.notes,
                updated_at = datetime('now')
        """
        self.execute(query, (scope, name, value, source, notes))

    # ========== Stories Operations ==========

    def create_story(
        self,
        title: str,
        description: Optional[str] = None,
        priority: int = 3,
        assignee: Optional[str] = None,
        labels: Optional[str] = None,
        acceptance_criteria: Optional[str] = None,
    ) -> int:
        """Create a new story."""
        query = """
            INSERT INTO stories
            (title, description, priority, assignee, labels, acceptance_criteria)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with self.connection() as conn:
            cursor = conn.execute(
                query,
                (title, description, priority, assignee, labels, acceptance_criteria),
            )
            return cursor.lastrowid

    def get_open_stories(self) -> List[Dict[str, Any]]:
        """Get all open stories."""
        query = """
            SELECT * FROM stories
            WHERE status IN ('todo', 'in_progress', 'blocked')
            ORDER BY priority ASC, created_at ASC
        """
        rows = self.execute(query)
        return [dict(row) for row in rows]

    # ========== Defects Operations ==========

    def create_defect(
        self,
        title: str,
        description: Optional[str] = None,
        severity: str = "major",
        detected_by: Optional[str] = None,
        story_id: Optional[int] = None,
    ) -> int:
        """Create a new defect."""
        query = """
            INSERT INTO defects (title, description, severity, detected_by, story_id)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.connection() as conn:
            cursor = conn.execute(query, (title, description, severity, detected_by, story_id))
            return cursor.lastrowid

    def get_open_defects(self) -> List[Dict[str, Any]]:
        """Get all open defects."""
        query = """
            SELECT * FROM defects
            WHERE status IN ('open', 'in_progress', 'blocked')
            ORDER BY
                CASE severity
                    WHEN 'critical' THEN 1
                    WHEN 'major' THEN 2
                    WHEN 'minor' THEN 4
                    ELSE 3
                END,
                created_at ASC
        """
        rows = self.execute(query)
        return [dict(row) for row in rows]

    def resolve_defect(self, defect_id: int, resolution: str, status: str = "resolved") -> None:
        """Resolve a defect."""
        query = """
            UPDATE defects
            SET status = ?, resolution = ?, resolved_at = datetime('now')
            WHERE id = ?
        """
        self.execute(query, (status, resolution, defect_id))

    # ========== Landmines Operations ==========

    def create_landmine(
        self,
        summary: str,
        cause: Optional[str] = None,
        impact: Optional[str] = None,
        detection: Optional[str] = None,
        remediation: Optional[str] = None,
        avoidance_rules: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> int:
        """Create a new landmine."""
        query = """
            INSERT INTO landmines
            (summary, cause, impact, detection, remediation, avoidance_rules, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self.connection() as conn:
            cursor = conn.execute(
                query,
                (summary, cause, impact, detection, remediation, avoidance_rules, tags),
            )
            return cursor.lastrowid

    def get_landmines(self, limit: int = 20, tags: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get recent landmines."""
        if tags:
            query = """
                SELECT * FROM landmines
                WHERE tags LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?
            """
            rows = self.execute(query, (f"%{tags}%", limit))
        else:
            query = """
                SELECT * FROM landmines
                ORDER BY updated_at DESC
                LIMIT ?
            """
            rows = self.execute(query, (limit,))
        return [dict(row) for row in rows]

    # ========== Views ==========

    def get_open_work(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get open work items (stories + defects)."""
        query = "SELECT * FROM v_open_work LIMIT ?"
        rows = self.execute(query, (limit,))
        return [dict(row) for row in rows]

    def get_defects_with_stories(self) -> List[Dict[str, Any]]:
        """Get defects with linked stories."""
        query = "SELECT * FROM v_defects_with_stories"
        rows = self.execute(query)
        return [dict(row) for row in rows]

    # ========== Utilities ==========

    def generate_trace_id(self) -> str:
        """Generate a unique trace ID for session tracking."""
        return str(uuid.uuid4())

    def backup(self, backup_path: str) -> bool:
        """Create a backup of the database."""
        try:
            import shutil

            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception:
            return False


# Global database instance
db = Database()
