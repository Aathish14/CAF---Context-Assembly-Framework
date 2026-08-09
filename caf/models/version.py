"""Version model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Version(BaseModel):
    """Version model representing an instruction version."""

    id: str = Field(..., description="Unique identifier for the version")
    instruction_id: str = Field(
        ..., description="ID of the instruction this version belongs to"
    )
    version_number: int = Field(..., description="Sequential version number")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when version was created",
    )
    created_by: str | None = Field(
        default=None, description="Identifier of who created this version"
    )
    change_summary: str = Field(..., description="Summary of changes in this version")
    parent_version_id: str | None = Field(
        default=None, description="ID of the parent version"
    )
