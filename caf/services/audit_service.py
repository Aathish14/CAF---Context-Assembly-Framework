"""Audit service for CAF application."""

import uuid
from datetime import UTC, datetime

from caf.models.audit_event import AuditEvent
from caf.repositories.base_repository import (
    InstructionRepositoryProtocol,
    VariantRepositoryProtocol,
    VersionRepositoryProtocol,
)


class AuditService:
    """Service for managing audit events."""

    def __init__(
        self,
        instruction_repository: InstructionRepositoryProtocol | None = None,
        version_repository: VersionRepositoryProtocol | None = None,
        variant_repository: VariantRepositoryProtocol | None = None,
    ):
        """Initialize the audit service.

        Args:
            instruction_repository: Optional instruction repository.
            version_repository: Optional version repository.
            variant_repository: Optional variant repository.
        """
        self._events: list[AuditEvent] = []
        self._instruction_repository = instruction_repository
        self._version_repository = version_repository
        self._variant_repository = variant_repository

    def log(
        self,
        event_type: str,
        entity_type: str,
        entity_id: str,
        performed_by: str | None = None,
        metadata: dict | None = None,
    ) -> AuditEvent:
        """Log an audit event.

        Args:
            event_type: Type of event (e.g., InstructionCreated, VersionCreated)
            entity_type: Type of entity (e.g., Instruction, Version, Variant)
            entity_id: ID of the entity affected
            performed_by: Optional identifier of who performed the action
            metadata: Optional additional metadata

        Returns:
            The created AuditEvent
        """
        event = AuditEvent(
            id=str(uuid.uuid4()),
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            performed_by=performed_by,
            timestamp=datetime.now(UTC),
            metadata=metadata or {},
        )
        self._events.append(event)
        return event

    def get_events(self) -> list[AuditEvent]:
        """Get all audit events in insertion order.

        Returns:
            List of all audit events
        """
        return self._events.copy()

    def get_events_for_entity(self, entity_id: str) -> list[AuditEvent]:
        """Get all audit events for a specific entity.

        Args:
            entity_id: ID of the entity

        Returns:
            List of audit events for the entity
        """
        return [event for event in self._events if event.entity_id == entity_id]

    def clear(self) -> None:
        """Clear all audit events."""
        self._events.clear()
