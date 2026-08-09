"""Variant service for CAF application."""

import uuid

from caf.models.variant import Variant
from caf.repositories.base_repository import VariantRepositoryProtocol
from caf.repositories.variant_repository import variant_repository


class VariantService:
    """Service for creating and managing instruction variants."""

    def __init__(self, variant_repository: VariantRepositoryProtocol):
        """Initialize VariantService.

        Args:
            variant_repository: Variant repository instance.
        """
        self._variant_repository = variant_repository

    def create_variant(
        self,
        version_id: str,
        variant_name: str,
        description: str | None = None,
        parent_variant: Variant | None = None,
    ) -> Variant:
        """Create a new variant for a version and persist it.

        Args:
            version_id: ID of the version this variant is based on.
            variant_name: Name of the variant.
            description: Optional description of the variant.
            parent_variant: Optional parent variant for lineage.

        Returns:
            Variant: New variant object.
        """
        parent_variant_id = parent_variant.id if parent_variant else None

        variant = Variant(
            id=str(uuid.uuid4()),
            version_id=version_id,
            variant_name=variant_name,
            description=description,
            parent_variant_id=parent_variant_id,
        )

        self._variant_repository.save(variant)
        return variant


# Global variant service instance for backward compatibility
variant_service = VariantService(variant_repository)
