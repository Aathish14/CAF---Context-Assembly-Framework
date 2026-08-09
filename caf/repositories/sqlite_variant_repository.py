"""SQLite-backed Variant repository for CAF application."""

from caf.models.variant import Variant
from caf.repositories.sqlite_base_repository import SQLiteBaseRepository


class SQLiteVariantRepository(SQLiteBaseRepository[Variant]):
    """SQLite-backed repository for Variant objects."""

    @property
    def table_name(self) -> str:
        return "variants"

    @property
    def id_column(self) -> str:
        return "id"

    @property
    def order_by_column(self) -> str:
        return "created_at"

    def _get_columns(self) -> list[str]:
        return [
            "id",
            "version_id",
            "variant_name",
            "description",
            "parent_variant_id",
            "created_at",
        ]

    def _model_to_row(self, variant: Variant) -> tuple:
        """Convert Variant to database row tuple."""
        return (
            variant.id,
            variant.version_id,
            variant.variant_name,
            variant.description,
            variant.parent_variant_id,
            self._to_db_datetime(variant.created_at),
        )

    def _row_to_model(self, row: dict) -> Variant:
        """Convert a database row to a Variant object."""
        return Variant(
            id=row["id"],
            version_id=row["version_id"],
            variant_name=row["variant_name"],
            description=row["description"],
            parent_variant_id=row["parent_variant_id"],
            created_at=self._from_db_datetime(row["created_at"]),
        )

    def get_by_version_id(self, version_id: str) -> list[Variant]:
        """Retrieve all variants for a specific version.

        Args:
            version_id: ID of the version.

        Returns:
            List of Variant objects for the version, in insertion order.
        """
        rows = self._execute_query(
            f"SELECT * FROM {self.table_name} WHERE version_id = ? ORDER BY created_at",
            (version_id,),
        )
        return [self._row_to_model(row) for row in rows]


# Global SQLite variant repository instance
sqlite_variant_repository = SQLiteVariantRepository()
