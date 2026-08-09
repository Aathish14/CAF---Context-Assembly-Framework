"""SQLite base repository for CAF application."""

from datetime import datetime
from typing import Any, TypeVar

from caf.database.db import get_db
from caf.repositories.base_repository import RepositoryProtocol

T = TypeVar("T")


class SQLiteBaseRepository[T](RepositoryProtocol[T]):
    """Base SQLite-backed repository with common CRUD operations."""

    def __init__(self) -> None:
        """Initialize the repository with database connection."""
        self._db = get_db()

    @property
    def table_name(self) -> str:
        """Override in child class: table name."""
        raise NotImplementedError

    @property
    def id_column(self) -> str:
        """Override in child class: primary key column name."""
        raise NotImplementedError

    @property
    def order_by_column(self) -> str:
        """Override in child class: default order by column."""
        raise NotImplementedError

    def _get_columns(self) -> list[str]:
        """Override in child class: list of column names in order."""
        raise NotImplementedError

    def _model_to_row(self, model: T) -> tuple:
        """Override in child class: convert model to row tuple."""
        raise NotImplementedError

    def _row_to_model(self, row: dict) -> T:
        """Override in child class: convert row dict to model."""
        raise NotImplementedError

    def _to_db_datetime(self, value: Any) -> str:
        """Convert a datetime value to database string format.

        Args:
            value: datetime object, ISO format string, or other.

        Returns:
            String in '%Y-%m-%d %H:%M:%S' format.
        """
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d %H:%M:%S")  # type: ignore[no-any-return]
        elif hasattr(value, "isoformat"):
            return value.isoformat()  # type: ignore[no-any-return]
        elif isinstance(value, str):
            return value
        else:
            return str(value)

    def _from_db_datetime(self, value: Any) -> Any:
        """Convert a database datetime string to datetime object.

        Args:
            value: String from database.

        Returns:
            datetime object if parsable, otherwise original value.
        """
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                pass
        return value

    def _build_upsert_query(self) -> str:
        """Build the INSERT ... ON CONFLICT query."""
        columns = self._get_columns()
        placeholders = ", ".join(["?"] * len(columns))
        update_clauses = ", ".join(
            [f"{col} = excluded.{col}" for col in columns if col != self.id_column]
        )
        return f"""
            INSERT INTO {self.table_name} ({", ".join(columns)})
            VALUES ({placeholders})
            ON CONFLICT({self.id_column}) DO UPDATE SET
                {update_clauses}
        """

    def _build_select_by_id(self) -> str:
        return f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ?"

    def _build_select_all(self) -> str:
        return f"SELECT * FROM {self.table_name} ORDER BY {self.order_by_column}"

    def _build_delete(self) -> str:
        return f"DELETE FROM {self.table_name} WHERE {self.id_column} = ?"

    def _execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        """Execute a SELECT query and return list of row dicts."""
        with self._db.get_connection() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def _execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows."""
        with self._db.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def save(self, model: T) -> None:
        """Save a model to the repository."""
        query = self._build_upsert_query()
        self._execute_update(query, self._model_to_row(model))

    def get_by_id(self, item_id: str) -> T:
        """Retrieve a model by ID.

        Args:
            item_id: ID of the model to retrieve.

        Returns:
            Model object.

        Raises:
            ValueError: If model with given ID does not exist.
        """
        rows = self._execute_query(self._build_select_by_id(), (item_id,))
        if not rows:
            raise ValueError(f"Item with id '{item_id}' not found")
        return self._row_to_model(rows[0])

    def get_all(self) -> list[T]:
        """Retrieve all models in order.

        Returns:
            List of all model objects.
        """
        rows = self._execute_query(self._build_select_all())
        return [self._row_to_model(row) for row in rows]

    def delete(self, item_id: str) -> None:
        """Delete a model by ID.

        Args:
            item_id: ID of the model to delete.

        Raises:
            ValueError: If model with given ID does not exist.
        """
        rows_affected = self._execute_update(self._build_delete(), (item_id,))
        if rows_affected == 0:
            raise ValueError(f"Item with id '{item_id}' not found")
