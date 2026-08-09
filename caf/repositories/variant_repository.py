"""Variant repository for CAF application."""

from caf.models.variant import Variant
from caf.repositories.base_repository import BaseRepository


class VariantRepository(BaseRepository[Variant]):
    """In-memory repository for Variant objects."""

    def get_by_version_id(self, version_id: str) -> list[Variant]:
        """Retrieve all variants for a specific version.

        Args:
            version_id: ID of the version.

        Returns:
            List of Variant objects for the version, in insertion order.
        """
        return [v for v in self.get_all() if v.version_id == version_id]


# Global variant repository instance
variant_repository = VariantRepository()
