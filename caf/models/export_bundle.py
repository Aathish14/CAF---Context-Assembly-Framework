"""Export bundle model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from caf.models.instruction import Instruction
from caf.models.variant import Variant
from caf.models.version import Version


class ExportBundle(BaseModel):
    """Complete export bundle for an instruction and its history."""

    instruction: Instruction = Field(..., description="The base instruction")
    versions: list[Version] = Field(
        default_factory=list, description="All versions of the instruction"
    )
    variants: list[Variant] = Field(
        default_factory=list, description="All variants across all versions"
    )
    exported_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the export was created",
    )
    exported_by: str | None = Field(
        default=None, description="Who performed the export"
    )
    schema_version: str = Field(default="1.0", description="Export schema version")
