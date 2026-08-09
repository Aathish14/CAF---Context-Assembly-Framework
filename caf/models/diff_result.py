"""Diff result model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from caf.models.version import Version


class DiffResult(BaseModel):
    """Result of comparing two versions."""

    old_version: Version = Field(..., description="The older version")
    new_version: Version = Field(..., description="The newer version")
    added_lines: list[str] = Field(
        default_factory=list, description="Lines added in new version"
    )
    removed_lines: list[str] = Field(
        default_factory=list, description="Lines removed from old version"
    )
    changed_lines: list[str] = Field(
        default_factory=list, description="Lines that changed between versions"
    )
    similarity_score: float = Field(..., description="Similarity score (0-100)")
    unified_diff: str = Field(..., description="Unified diff format string")
    compared_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When comparison was performed",
    )

    @property
    def has_changes(self) -> bool:
        """Check if there are any changes between versions."""
        return (
            len(self.added_lines) > 0
            or len(self.removed_lines) > 0
            or len(self.changed_lines) > 0
        )
