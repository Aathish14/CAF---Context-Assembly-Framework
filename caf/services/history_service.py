"""History service for CAF application for CAF application."""

from caf.models.instruction_history import InstructionHistory
from caf.models.variant import Variant
from caf.models.version import Version
from caf.repositories.base_repository import (
    InstructionRepositoryProtocol,
    VariantRepositoryProtocol,
    VersionRepositoryProtocol,
)
from caf.services.audit_service import AuditService
from caf.services.variant_service import VariantService
from caf.services.version_service import VersionService


class HistoryService:
    """Service for managing instruction history including versions and variants."""

    def __init__(
        self,
        version_service: "VersionService",
        variant_service: "VariantService",
        instruction_repository: InstructionRepositoryProtocol,
        version_repository: VersionRepositoryProtocol,
        variant_repository: VariantRepositoryProtocol,
        audit_service: "AuditService",
    ):
        """Initialize the history service.

        Args:
            version_service: Service for managing versions.
            variant_service: Service for managing variants.
            instruction_repository: Repository for instructions.
            version_repository: Repository for versions.
            variant_repository: Repository for variants.
            audit_service: Service for logging audit events.
        """
        self._version_service = version_service
        self._variant_service = variant_service
        self._instruction_repository = instruction_repository
        self._version_repository = version_repository
        self._variant_repository = variant_repository
        self._audit_service = audit_service

    def get_history(self, instruction_id: str) -> InstructionHistory:
        """Get complete history for an instruction.

        Args:
            instruction_id: ID of the instruction.

        Returns:
            InstructionHistory containing instruction, versions, and variants.

        Raises:
            ValueError: If instruction not found.
        """
        instruction = self._instruction_repository.get_by_id(instruction_id)
        versions = self._version_repository.get_by_instruction_id(instruction_id)
        variants_by_version = {}

        for version in versions:
            variants = self._variant_repository.get_by_version_id(version.id)
            variants_by_version[version.id] = variants

        # Log audit event
        self._audit_service.log(
            event_type="HistoryRetrieved",
            entity_type="Instruction",
            entity_id=instruction_id,
        )

        return InstructionHistory(
            instruction=instruction,
            versions=versions,
            variants_by_version=variants_by_version,
        )

    def get_latest_version(self, instruction_id: str) -> Version:
        """Get the latest version for an instruction.

        Args:
            instruction_id: ID of the instruction.

        Returns:
            The latest Version.

        Raises:
            ValueError: If no versions exist for the instruction.
        """
        versions = self._version_repository.get_by_instruction_id(instruction_id)
        if not versions:
            raise ValueError(f"No versions found for instruction {instruction_id}")
        latest = versions[-1]

        # Log audit event
        self._audit_service.log(
            event_type="LatestVersionRequested",
            entity_type="Instruction",
            entity_id=instruction_id,
        )

        return latest

    def create_new_version(
        self,
        instruction_id: str,
        change_summary: str,
        created_by: str,
    ) -> Version:
        """Create a new version for an instruction.

        Args:
            instruction_id: ID of the instruction.
            change_summary: Summary of changes.
            created_by: Identifier of who created this version.

        Returns:
            The newly created Version.
        """
        latest_version = self.get_latest_version(instruction_id)
        return self._version_service.create_version(
            instruction_id=instruction_id,
            change_summary=change_summary,
            created_by=created_by,
            parent_version=latest_version,
        )

    def add_variant(
        self,
        version_id: str,
        variant_name: str,
        description: str | None = None,
    ) -> Variant:
        """Add a variant to a version.

        Args:
            version_id: ID of the version to add variant to.
            variant_name: Name of the variant.
            description: Optional description of the variant.

        Returns:
            The newly created Variant.
        """
        return self._variant_service.create_variant(
            version_id=version_id,
            variant_name=variant_name,
            description=description,
            parent_variant=None,
        )

    def add_variant_with_parent(
        self,
        version_id: str,
        variant_name: str,
        description: str | None,
        parent_variant_id: str,
    ) -> Variant:
        """Add a variant with a parent variant.

        Args:
            version_id: ID of the version to add variant to.
            variant_name: Name of the variant.
            description: Optional description of the variant.
            parent_variant_id: ID of the parent variant.

        Returns:
            The newly created Variant.
        """
        parent_variant = self._variant_repository.get_by_id(parent_variant_id)
        return self._variant_service.create_variant(
            version_id=version_id,
            variant_name=variant_name,
            description=description,
            parent_variant=parent_variant,
        )
