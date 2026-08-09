"""CAF Repositories package."""

# In-memory repositories
from caf.repositories.base_repository import (
    BaseRepository,
    InstructionRepositoryProtocol,
    VariantRepositoryProtocol,
    VersionRepositoryProtocol,
)
from caf.repositories.instruction_repository import (
    InstructionRepository,
    instruction_repository,
)

# SQLite repositories
from caf.repositories.sqlite_base_repository import SQLiteBaseRepository
from caf.repositories.sqlite_instruction_repository import (
    SQLiteInstructionRepository,
    sqlite_instruction_repository,
)
from caf.repositories.sqlite_variant_repository import (
    SQLiteVariantRepository,
    sqlite_variant_repository,
)
from caf.repositories.sqlite_version_repository import (
    SQLiteVersionRepository,
    sqlite_version_repository,
)
from caf.repositories.variant_repository import VariantRepository, variant_repository
from caf.repositories.version_repository import VersionRepository, version_repository

__all__ = [
    "BaseRepository",
    "InstructionRepository",
    "instruction_repository",
    "VersionRepository",
    "version_repository",
    "VariantRepository",
    "variant_repository",
    "SQLiteBaseRepository",
    "SQLiteInstructionRepository",
    "sqlite_instruction_repository",
    "SQLiteVersionRepository",
    "sqlite_version_repository",
    "SQLiteVariantRepository",
    "sqlite_variant_repository",
    "InstructionRepositoryProtocol",
    "VariantRepositoryProtocol",
    "VersionRepositoryProtocol",
]
