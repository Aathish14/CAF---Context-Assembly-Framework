"""Database connection and session management."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from caf.config import settings

if TYPE_CHECKING:
    pass


def _convert_timestamp(value: bytes | str) -> datetime:
    """Convert SQLite TIMESTAMP to timezone-aware datetime (UTC)."""
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    if isinstance(value, str):
        # Handle both 'YYYY-MM-DD HH:MM:SS' and 'YYYY-MM-DD HH:MM:SS.ffffff' formats
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            # Fallback for 'YYYY-MM-DD HH:MM:SS' format
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return dt.replace(tzinfo=UTC)
    raise ValueError(f"Cannot convert {value!r} to datetime")


def _convert_date(value: bytes | str) -> datetime:
    """Convert SQLite DATE to timezone-aware datetime (UTC)."""
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.replace(tzinfo=UTC)
    raise ValueError(f"Cannot convert {value!r} to datetime")


# Register custom converters for timezone-aware datetime handling
sqlite3.register_converter("TIMESTAMP", _convert_timestamp)
sqlite3.register_converter("DATETIME", _convert_timestamp)
sqlite3.register_converter("DATE", _convert_date)


class Database:
    """Database manager for SQLite connection."""

    def __init__(self, db_path: str | None = None):
        """Initialize database manager.

        Args:
            db_path: Path to SQLite database file. If None, uses settings.
        """
        raw_url = getattr(settings, "DATABASE_URL", "sqlite:///./caf.db")
        assert isinstance(raw_url, str)
        db_url: str = db_path or raw_url
        # Handle sqlite:/// prefix
        if db_url.startswith("sqlite:///"):
            db_url = db_url[9:]  # Remove sqlite:/// prefix

        self.db_path: str = db_url

        # Ensure directory exists
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        self._connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """Create or get database connection.

        Returns:
            SQLite connection object.
        """
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.db_path,
                detect_types=sqlite3.PARSE_COLNAMES,
            )
            # Enable foreign key constraints
            self._connection.execute("PRAGMA foreign_keys = ON")
            # Return rows as dictionaries
            self._connection.row_factory = sqlite3.Row
        # _connection can be _ConnectionWrapper during transactions
        return self._connection

    def close(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connection.

        Yields:
            SQLite connection object.
        """
        conn = self.connect()
        try:
            yield conn
        finally:
            # Don't close the connection here - keep it open for reuse
            pass

    def execute_script(self, sql_script: str) -> None:
        """Execute a SQL script.

        Args:
            sql_script: SQL script to execute.
        """
        with self.get_connection() as conn:
            conn.executescript(sql_script)
            conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute a SELECT query and return results.

        Args:
            query: SQL query to execute.
            params: Query parameters.

        Returns:
            List of rows as dictionaries.
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query.

        Args:
            query: SQL query to execute.
            params: Query parameters.

        Returns:
            Number of affected rows.
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount


# Global database instance
db = Database()


def get_db() -> Database:
    """Get database instance.

    Returns:
        Database instance.
    """
    return db


def init_db() -> None:
    """Initialize database with schema."""
    # Read schema.sql and execute it
    schema_path = Path(__file__).parent / "schema.sql"
    if schema_path.exists():
        with open(schema_path, encoding="utf-8") as f:
            schema = f.read()
        db.execute_script(schema)
    else:
        raise FileNotFoundError(f"Schema file not found: {schema_path}")


def close_db() -> None:
    """Close database connection."""
    db.close()
