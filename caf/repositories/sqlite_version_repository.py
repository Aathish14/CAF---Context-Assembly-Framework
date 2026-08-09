"""SQLite-backed Version repository for CAF application."""

from caf.models.version import Version
from caf.repositories.sqlite_base_repository import SQLiteBaseRepository


class SQLiteVersionRepository(SQLiteBaseRepository[Version]):
    """SQLite-backed repository for Version objects."""

    @property
    def table_name(self) -> str:
        return "versions"

    @property
    def id_column(self) -> str:
        return "id"

    @property
    def order_by_column(self) -> str:
        return "created_at"

    def _get_columns(self) -> list[str]:
        return [
            "id",
            "instruction_id",
            "version_number",
            "change_summary",
            "created_by",
            "created_at",
            "parent_version_id",
        ]

    def _model_to_row(self, version: Version) -> tuple:
        """Convert Version to database row tuple."""
        return (
            version.id,
            version.instruction_id,
            version.version_number,
            version.change_summary,
            version.created_by,
            self._to_db_datetime(version.created_at),
            version.parent_version_id,
        )

    def _row_to_model(self, row: dict) -> Version:
        """Convert a database row to a Version object."""
        return Version(
            id=row["id"],
            instruction_id=row["instruction_id"],
            version_number=row["version_number"],
            change_summary=row["change_summary"],
            created_by=row["created_by"],
            created_at=self._from_db_datetime(row["created_at"]),
            parent_version_id=row["parent_version_id"],
        )

    def get_by_instruction_id(self, instruction_id: str) -> list[Version]:
        """Retrieve all versions for a specific instruction.

        Args:
            instruction_id: ID of the instruction.

        Returns:
            List of Version objects for the instruction, ordered by version_number.
        """
        rows = self._execute_query(
            f"SELECT * FROM {self.table_name} WHERE instruction_id = ? ORDER BY version_number",
            (instruction_id,),
        )
        return [self._row_to_model(row) for row in rows]


# Global SQLite version repository instance
sqlite_version_repository = SQLiteVersionRepository()
