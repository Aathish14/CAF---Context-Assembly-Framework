"""CAF Dependency Injection Container."""

from caf.repositories.base_repository import (
    InstructionRepositoryProtocol,
    VariantRepositoryProtocol,
    VersionRepositoryProtocol,
)
from caf.repositories.instruction_repository import InstructionRepository
from caf.repositories.sqlite_instruction_repository import SQLiteInstructionRepository
from caf.repositories.sqlite_variant_repository import SQLiteVariantRepository
from caf.repositories.sqlite_version_repository import SQLiteVersionRepository
from caf.repositories.variant_repository import VariantRepository
from caf.repositories.version_repository import VersionRepository
from caf.services.audit_service import AuditService
from caf.services.context_builder import ContextBuilder
from caf.services.diff_service import DiffService
from caf.services.export_import_service import ExportImportService
from caf.services.history_service import HistoryService
from caf.services.instruction_builder import InstructionBuilder
from caf.services.instruction_pipeline import InstructionPipeline
from caf.services.question_service import QuestionService
from caf.services.template_service import TemplateService
from caf.services.validation_service import ValidationService
from caf.services.variant_service import VariantService
from caf.services.version_service import VersionService


class Container:
    """Lightweight dependency injection container for CAF."""

    def __init__(
        self,
        use_sqlite: bool = False,
        instruction_repo: InstructionRepositoryProtocol | None = None,
        version_repo: VersionRepositoryProtocol | None = None,
        variant_repo: VariantRepositoryProtocol | None = None,
    ):
        """Initialize the container.

        Args:
            use_sqlite: Whether to use SQLite repositories (default: in-memory)
            instruction_repo: Optional custom instruction repository
            version_repo: Optional custom version repository
            variant_repo: Optional custom variant repository
        """
        self._use_sqlite = use_sqlite
        self._repos_created = False
        self._services_created = False

        # Repository instances
        self._instruction_repo = instruction_repo
        self._version_repo = version_repo
        self._variant_repo = variant_repo

        # Service instances
        self._question_service: QuestionService | None = None
        self._validation_service: ValidationService | None = None
        self._context_builder: ContextBuilder | None = None
        self._template_service: TemplateService | None = None
        self._instruction_builder: InstructionBuilder | None = None
        self._version_service: VersionService | None = None
        self._variant_service: VariantService | None = None
        self._instruction_pipeline: InstructionPipeline | None = None
        self._history_service: HistoryService | None = None
        self._diff_service: DiffService | None = None
        self._audit_service: AuditService | None = None
        self._export_import_service: ExportImportService | None = None

    # ==================== Repository Properties ====================

    @property
    def instruction_repository(self) -> InstructionRepositoryProtocol:
        """Get or create instruction repository."""
        if self._instruction_repo is None:
            if self._use_sqlite:
                self._instruction_repo = SQLiteInstructionRepository()
            else:
                self._instruction_repo = InstructionRepository()
        return self._instruction_repo

    @property
    def version_repository(self) -> VersionRepositoryProtocol:
        """Get or create version repository."""
        if self._version_repo is None:
            if self._use_sqlite:
                self._version_repo = SQLiteVersionRepository()
            else:
                self._version_repo = VersionRepository()
        return self._version_repo

    @property
    def variant_repository(self) -> VariantRepositoryProtocol:
        """Get or create variant repository."""
        if self._variant_repo is None:
            if self._use_sqlite:
                self._variant_repo = SQLiteVariantRepository()
            else:
                self._variant_repo = VariantRepository()
        return self._variant_repo

    # ==================== Service Properties ====================

    @property
    def question_service(self) -> QuestionService:
        """Get or create question service."""
        if self._question_service is None:
            self._question_service = QuestionService()
        return self._question_service

    @property
    def validation_service(self) -> ValidationService:
        """Get or create validation service."""
        if self._validation_service is None:
            self._validation_service = ValidationService()
        return self._validation_service

    @property
    def context_builder(self) -> ContextBuilder:
        """Get or create context builder."""
        if self._context_builder is None:
            self._context_builder = ContextBuilder()
        return self._context_builder

    @property
    def template_service(self) -> TemplateService:
        """Get or create template service."""
        if self._template_service is None:
            self._template_service = TemplateService()
        return self._template_service

    @property
    def instruction_builder(self) -> InstructionBuilder:
        """Get or create instruction builder."""
        if self._instruction_builder is None:
            self._instruction_builder = InstructionBuilder(
                template_service=self.template_service
            )
        return self._instruction_builder

    @property
    def version_service(self) -> VersionService:
        """Get or create version service."""
        if self._version_service is None:
            self._version_service = VersionService(
                version_repository=self.version_repository
            )
        return self._version_service

    @property
    def variant_service(self) -> VariantService:
        """Get or create variant service."""
        if self._variant_service is None:
            self._variant_service = VariantService(
                variant_repository=self.variant_repository
            )
        return self._variant_service

    @property
    def instruction_pipeline(self) -> InstructionPipeline:
        """Get or create instruction pipeline."""
        if self._instruction_pipeline is None:
            self._instruction_pipeline = InstructionPipeline(
                validation_service=self.validation_service,
                context_builder=self.context_builder,
                instruction_builder=self.instruction_builder,
                version_service=self.version_service,
                variant_service=self.variant_service,
                instruction_repository=self.instruction_repository,
                version_repository=self.version_repository,
                variant_repository=self.variant_repository,
                audit_service=self.audit_service,
            )
        return self._instruction_pipeline

    @property
    def history_service(self) -> HistoryService:
        """Get or create history service."""
        if self._history_service is None:
            self._history_service = HistoryService(
                version_service=self.version_service,
                variant_service=self.variant_service,
                instruction_repository=self.instruction_repository,
                version_repository=self.version_repository,
                variant_repository=self.variant_repository,
                audit_service=self.audit_service,
            )
        return self._history_service

    @property
    def diff_service(self) -> DiffService:
        """Get or create diff service."""
        if self._diff_service is None:
            self._diff_service = DiffService(
                version_repository=self.version_repository,
                version_service=self.version_service,
                history_service=self.history_service,
                audit_service=self.audit_service,
            )
        return self._diff_service

    @property
    def audit_service(self) -> AuditService:
        """Get or create audit service."""
        if self._audit_service is None:
            self._audit_service = AuditService(
                instruction_repository=self.instruction_repository,
                version_repository=self.version_repository,
                variant_repository=self.variant_repository,
            )
        return self._audit_service

    @property
    def export_import_service(self) -> ExportImportService:
        """Get or create export/import service."""
        if self._export_import_service is None:
            self._export_import_service = ExportImportService(
                instruction_repository=self.instruction_repository,
                version_repository=self.version_repository,
                variant_repository=self.variant_repository,
            )
        return self._export_import_service

    def reset(self) -> None:
        """Reset all cached instances (useful for testing)."""
        self._instruction_repo = None
        self._version_repo = None
        self._variant_repo = None
        self._question_service = None
        self._validation_service = None
        self._context_builder = None
        self._template_service = None
        self._instruction_builder = None
        self._version_service = None
        self._variant_service = None
        self._instruction_pipeline = None
        self._history_service = None
        self._diff_service = None
        self._audit_service = None
        self._export_import_service = None
        self._repos_created = False
        self._services_created = False


# Default container instance for backward compatibility
default_container = Container()


def get_container() -> Container:
    """Get the default container instance."""
    return default_container
