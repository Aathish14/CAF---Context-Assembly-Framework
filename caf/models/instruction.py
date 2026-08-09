"""Instruction model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Instruction(BaseModel):
    """Instruction model representing an assembled instruction."""

    id: str = Field(..., description="Unique identifier for the instruction")
    template_name: str = Field(..., description="Name of the template used")
    context: dict = Field(..., description="Context data used for assembly")
    assembled_instruction: str = Field(
        ..., description="The fully assembled instruction text"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when instruction was created",
    )
    version: int = Field(default=1, description="Version number of the instruction")
