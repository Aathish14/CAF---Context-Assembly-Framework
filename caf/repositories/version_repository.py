"""Version repository for CAF application."""

from caf.models.version import Version
from caf.repositories.base_repository import BaseRepository


class VersionRepository(BaseRepository[Version]):
    """In-memory repository for Version objects."""

    def get_by_instruction_id(self, instruction_id: str) -> list[Version]:
        """Retrieve all versions for a specific instruction.

        Args:
            instruction_id: ID of the instruction to get versions for.

        Returns:
            List of Version objects for the instruction, ordered by version_number.
        """
        versions = [
            v for v in self._items.values() if v.instruction_id == instruction_id
        ]
        return sorted(versions, key=lambda v: v.version_number)


# Global version repository instance
version_repository = VersionRepository()
