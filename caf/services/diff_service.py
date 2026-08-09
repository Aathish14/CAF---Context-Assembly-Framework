"""Diff service for CAF application."""

import difflib

from caf.models.diff_result import DiffResult
from caf.models.version import Version
from caf.repositories.base_repository import VersionRepositoryProtocol
from caf.services.audit_service import AuditService
from caf.services.history_service import HistoryService
from caf.services.version_service import VersionService


class DiffService:
    """Service for comparing instruction versions."""

    def __init__(
        self,
        version_repository: VersionRepositoryProtocol,
        version_service: "VersionService",
        history_service: "HistoryService",
        audit_service: "AuditService",
    ):
        """Initialize the diff service.

        Args:
            version_repository: Repository for versions.
            version_service: Service for managing versions.
            history_service: Service for history operations.
            audit_service: Service for logging audit events.
        """
        self._version_repository = version_repository
        self._version_service = version_service
        self._history_service = history_service
        self._audit_service = audit_service

    def _get_version_text(self, version: Version) -> str:
        """Get the instruction text for a version."""
        # The version itself doesn't store the full instruction text.
        # We need to get it from the instruction repository.
        # For now, we'll use the change_summary as a proxy, but ideally
        # we'd need the actual instruction text.
        return version.change_summary

    def _compute_diff(self, old_text: str, new_text: str) -> tuple:
        """Compute diff between two texts using difflib."""
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)

        diff = list(
            difflib.unified_diff(
                old_lines, new_lines, lineterm="", fromfile="old", tofile="new"
            )
        )

        added: list[str] = []
        removed: list[str] = []
        changed: list[str] = []

        # Parse the diff to categorize changes
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                added.append(line[1:])
            elif line.startswith("-") and not line.startswith("---"):
                removed.append(line[1:])

        # For changed lines, we'll use a simple heuristic:
        # If a line was removed and a line was added at similar position,
        # consider it a change.
        # For simplicity, we'll mark lines that appear in both added and removed
        # as changed (this is a simplification).

        return added, removed, changed, "\n".join(diff)

    def _calculate_similarity(self, old_text: str, new_text: str) -> float:
        """Calculate similarity score between two texts (0-100)."""
        if not old_text and not new_text:
            return 100.0
        if not old_text or not new_text:
            return 0.0

        # Use SequenceMatcher for similarity
        matcher = difflib.SequenceMatcher(None, old_text, new_text)
        return matcher.ratio() * 100

    def compare_versions(self, version_a_id: str, version_b_id: str) -> DiffResult:
        """Compare two versions.

        Args:
            version_a_id: ID of the first version.
            version_b_id: ID of the second version.

        Returns:
            DiffResult containing the comparison.

        Raises:
            ValueError: If either version not found.
        """
        version_a = self._version_repository.get_by_id(version_a_id)
        version_b = self._version_repository.get_by_id(version_b_id)

        # Determine which is older based on version_number
        if version_a.version_number < version_b.version_number:
            old_version = version_a
            new_version = version_b
        else:
            old_version = version_b
            new_version = version_a

        old_text = self._get_version_text(old_version)
        new_text = self._get_version_text(new_version)

        added_lines, removed_lines, changed_lines, unified_diff = self._compute_diff(
            old_text, new_text
        )
        similarity_score = self._calculate_similarity(old_text, new_text)

        # Log audit event
        self._audit_service.log(
            event_type="VersionsCompared",
            entity_type="Version",
            entity_id=f"{version_a_id},{version_b_id}",
        )

        return DiffResult(
            old_version=old_version,
            new_version=new_version,
            added_lines=added_lines,
            removed_lines=removed_lines,
            changed_lines=changed_lines,
            similarity_score=similarity_score,
            unified_diff=unified_diff,
        )

    def compare_latest(self, instruction_id: str) -> DiffResult:
        """Compare the latest version against its parent.

        Args:
            instruction_id: ID of the instruction.

        Returns:
            DiffResult comparing latest version with its parent.

        Raises:
            ValueError: If instruction has no versions or only one version.
        """
        latest_version = self._history_service.get_latest_version(instruction_id)

        if latest_version.parent_version_id is None:
            raise ValueError(
                f"Latest version {latest_version.id} has no parent to compare against"
            )

        parent_version = self._history_service._version_repository.get_by_id(
            latest_version.parent_version_id
        )

        # Log audit event
        self._audit_service.log(
            event_type="VersionsCompared",
            entity_type="Instruction",
            entity_id=instruction_id,
        )

        return self.compare_versions(parent_version.id, latest_version.id)

    def get_version_chain(self, instruction_id: str) -> list[DiffResult]:
        """Get diff results for the entire version chain.

        Args:
            instruction_id: ID of the instruction.

        Returns:
            List of DiffResult for each consecutive version pair.
        """
        history = self._history_service.get_history(instruction_id)
        results = []

        for i in range(1, len(history.versions)):
            diff = self.compare_versions(
                history.versions[i - 1].id, history.versions[i].id
            )
            results.append(diff)

        return results
