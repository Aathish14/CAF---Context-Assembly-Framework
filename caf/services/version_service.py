"""Version service for CAF application."""

import uuid

from caf.models.version import Version
from caf.repositories.base_repository import VersionRepositoryProtocol
from caf.repositories.version_repository import version_repository


class VersionService:
    """Service for creating and managing instruction versions."""

    def __init__(self, version_repository: VersionRepositoryProtocol):
        """Initialize VersionService.

        Args:
            version_repository: Version repository instance.
        """
        self._version_repository = version_repository

    def create_version(
        self,
        instruction_id: str,
        change_summary: str,
        created_by: str | None = None,
        parent_version: Version | None = None,
    ) -> Version:
        """Create a new version for an instruction and persist it.

        Args:
            instruction_id: ID of the instruction this version belongs to.
            change_summary: Summary of changes in this version.
            created_by: Optional identifier of who created this version.
            parent_version: Optional parent version for sequential numbering.

        Returns:
            Version: New version object.
        """
        if parent_version is None:
            version_number = 1
            parent_version_id = None
        else:
            version_number = parent_version.version_number + 1
            parent_version_id = parent_version.id

        version = Version(
            id=str(uuid.uuid4()),
            instruction_id=instruction_id,
            version_number=version_number,
            created_by=created_by,
            change_summary=change_summary,
            parent_version_id=parent_version_id,
        )

        self._version_repository.save(version)
        return version


# Global version service instance for backward compatibility
version_service = VersionService(version_repository)
