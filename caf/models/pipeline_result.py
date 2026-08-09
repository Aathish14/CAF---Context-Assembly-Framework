"""Pipeline result model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from caf.models.instruction import Instruction
from caf.models.variant import Variant
from caf.models.version import Version


class PipelineResult(BaseModel):
    """Result of the instruction pipeline execution."""

    instruction: Instruction | None = Field(
        default=None, description="The created instruction"
    )
    version: Version | None = Field(default=None, description="The initial version")
    variant: Variant | None = Field(default=None, description="The created variant")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Pipeline execution timestamp",
    )
    success: bool = Field(
        default=True, description="Whether pipeline completed successfully"
    )
    error: str | None = Field(
        default=None, description="Error message if pipeline failed"
    )
