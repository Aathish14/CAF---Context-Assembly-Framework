"""Instruction history model for CAF application."""

from pydantic import BaseModel, Field

from caf.models.instruction import Instruction
from caf.models.variant import Variant
from caf.models.version import Version


class InstructionHistory(BaseModel):
    """Complete history for an instruction including versions and variants."""

    instruction: Instruction = Field(..., description="The base instruction")
    versions: list[Version] = Field(
        default_factory=list, description="All versions ordered by version_number"
    )
    variants_by_version: dict[str, list[Variant]] = Field(
        default_factory=dict, description="Variants grouped by version_id"
    )

    @property
    def latest_version(self) -> "Version | None":
        """Get the latest version."""
        if not self.versions:
            return None
        return self.versions[-1]

    @property
    def version_count(self) -> int:
        """Get total number of versions."""
        return len(self.versions)

    @property
    def total_variants(self) -> int:
        """Get total number of variants across all versions."""
        return sum(len(variants) for variants in self.variants_by_version.values())
