"""Variant model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Variant(BaseModel):
    """Variant model representing an instruction variant."""

    id: str = Field(..., description="Unique identifier for the variant")
    version_id: str = Field(
        ..., description="ID of the version this variant is based on"
    )
    variant_name: str = Field(..., description="Name of the variant")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when variant was created",
    )
    parent_variant_id: str | None = Field(
        default=None, description="ID of the parent variant"
    )
    description: str | None = Field(
        default=None, description="Description of the variant"
    )
