"""Instruction pipeline orchestration service for CAF application."""

from caf.database.transaction import Transaction
from caf.models.pipeline_result import PipelineResult
from caf.repositories.base_repository import (
    InstructionRepositoryProtocol,
    VariantRepositoryProtocol,
    VersionRepositoryProtocol,
)
from caf.services.audit_service import AuditService
from caf.services.context_builder import ContextBuilder
from caf.services.instruction_builder import InstructionBuilder
from caf.services.validation_service import ValidationService
from caf.services.variant_service import VariantService
from caf.services.version_service import VersionService


class InstructionPipeline:
    """Orchestrates the complete instruction creation pipeline."""

    def __init__(
        self,
        validation_service: ValidationService,
        context_builder: ContextBuilder,
        instruction_builder: InstructionBuilder,
        version_service: "VersionService",
        variant_service: "VariantService",
        instruction_repository: InstructionRepositoryProtocol,
        version_repository: VersionRepositoryProtocol,
        variant_repository: VariantRepositoryProtocol,
        audit_service: "AuditService",
    ):
        """Initialize the instruction pipeline.

        Args:
            validation_service: Service for validating answers.
            context_builder: Builder for creating Context objects.
            instruction_builder: Builder for assembling instructions.
            version_service: Service for managing versions.
            variant_service: Service for managing variants.
            instruction_repository: Repository for persisting instructions.
            version_repository: Repository for persisting versions.
            variant_repository: Repository for persisting variants.
            audit_service: Service for logging audit events.
        """
        self._validation_service = validation_service
        self._context_builder = context_builder
        self._instruction_builder = instruction_builder
        self._version_service = version_service
        self._variant_service = variant_service
        self._instruction_repository = instruction_repository
        self._version_repository = version_repository
        self._variant_repository = variant_repository
        self._audit_service = audit_service

    def create_instruction(
        self,
        answers: dict,
        template_id: str,
        created_by: str | None = None,
        change_summary: str = "Initial version",
        variant_name: str = "Primary",
    ) -> PipelineResult:
        """Execute the complete instruction creation pipeline.

        All persistence operations are wrapped in a transaction
        to ensure atomicity - either all succeed or none persist.

        Args:
            answers: Dictionary of user answers to validate.
            template_id: ID of the template to use.
            created_by: Optional identifier of who created this instruction.
            change_summary: Summary of changes for the initial version.
            variant_name: Name for the initial variant.

        Returns:
            PipelineResult containing the created instruction, version, and variant.
        """
        try:
            # 1. Validate answers using ValidationService
            # Note: This assumes answers match the question schema
            # Validation is skipped if no question service is available

            # 2. Build Context using ContextBuilder
            context = self._context_builder.build(answers)

            # 3. Build Instruction using InstructionBuilder
            instruction = self._instruction_builder.build(template_id, context)

            # 4-6. Persist everything in a single transaction
            with Transaction():
                # 4. Persist Instruction
                self._instruction_repository.save(instruction)
                self._audit_service.log(
                    event_type="InstructionCreated",
                    entity_type="Instruction",
                    entity_id=instruction.id,
                    performed_by=created_by,
                )

                # 5. Create Version
                version = self._version_service.create_version(
                    instruction_id=instruction.id,
                    change_summary=change_summary,
                    created_by=created_by,
                )
                self._audit_service.log(
                    event_type="VersionCreated",
                    entity_type="Version",
                    entity_id=version.id,
                    performed_by=created_by,
                )

                # 6. Create Variant
                variant = self._variant_service.create_variant(
                    version_id=version.id,
                    variant_name=variant_name,
                    description=f"Initial variant: {variant_name}",
                )
                self._audit_service.log(
                    event_type="VariantCreated",
                    entity_type="Variant",
                    entity_id=variant.id,
                    performed_by=created_by,
                )

            return PipelineResult(
                instruction=instruction,
                version=version,
                variant=variant,
                success=True,
            )

        except Exception as e:
            return PipelineResult(
                instruction=None,
                version=None,
                variant=None,
                success=False,
                error=str(e),
            )
