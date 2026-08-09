"""Audit event model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    """Represents an audit event in the system."""

    id: str = Field(..., description="Unique identifier for the audit event")
    event_type: str = Field(
        ..., description="Type of event (e.g., InstructionCreated, VersionCreated)"
    )
    entity_type: str = Field(
        ..., description="Type of entity (e.g., Instruction, Version, Variant)"
    )
    entity_id: str = Field(..., description="ID of the entity affected")
    performed_by: str | None = Field(
        default=None, description="Identifier of who performed the action"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the event occurred",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Additional event metadata"
    )
