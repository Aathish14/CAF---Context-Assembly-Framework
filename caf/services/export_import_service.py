"""Export/Import service for CAF application."""

from caf.models.export_bundle import ExportBundle
from caf.repositories.base_repository import (
    InstructionRepositoryProtocol,
    VariantRepositoryProtocol,
    VersionRepositoryProtocol,
)


class ExportImportService:
    """Service for exporting and importing instruction bundles."""

    def __init__(
        self,
        instruction_repository: InstructionRepositoryProtocol,
        version_repository: VersionRepositoryProtocol,
        variant_repository: VariantRepositoryProtocol,
    ):
        """Initialize the export/import service.

        Args:
            instruction_repository: Repository for instructions.
            version_repository: Repository for versions.
            variant_repository: Repository for variants.
        """
        self._instruction_repository = instruction_repository
        self._version_repository = version_repository
        self._variant_repository = variant_repository

    def export_instruction(self, instruction_id: str) -> ExportBundle:
        """Export an instruction and all its history.

        Args:
            instruction_id: ID of the instruction to export.

        Returns:
            ExportBundle containing the instruction and all its history.

        Raises:
            ValueError: If instruction not found.
        """
        instruction = self._instruction_repository.get_by_id(instruction_id)
        versions = self._version_repository.get_by_instruction_id(instruction_id)

        variants = []
        for version in versions:
            version_variants = self._variant_repository.get_by_version_id(version.id)
            variants.extend(version_variants)

        return ExportBundle(
            instruction=instruction,
            versions=versions,
            variants=variants,
        )

    def export_json(self, instruction_id: str) -> str:
        """Export an instruction as pretty JSON.

        Args:
            instruction_id: ID of the instruction to export.

        Returns:
            Pretty JSON string (indent=2, exclude_none=True).
        """
        bundle = self.export_instruction(instruction_id)
        return bundle.model_dump_json(indent=2, exclude_none=True)

    def import_bundle(self, bundle: ExportBundle) -> ExportBundle:
        """Import an export bundle, replacing existing records if they exist.

        Args:
            bundle: ExportBundle to import.

        Returns:
            The imported ExportBundle (same as input).
        """
        # Save instruction (will replace if exists)
        self._instruction_repository.save(bundle.instruction)

        # Save versions (will replace if exists)
        for version in bundle.versions:
            self._version_repository.save(version)

        # Save variants (will replace if exists)
        for variant in bundle.variants:
            self._variant_repository.save(variant)

        return bundle

    def import_json(self, json_string: str) -> ExportBundle:
        """Import an export bundle from JSON string.

        Args:
            json_string: JSON string to parse and import.

        Returns:
            The imported ExportBundle.
        """
        bundle = ExportBundle.model_validate_json(json_string)
        return self.import_bundle(bundle)
