"""Tests for HistoryService."""

import pytest

from caf.core.container import Container
from caf.models.instruction import Instruction
from caf.models.instruction_history import InstructionHistory


class TestHistoryService:
    """Tests for HistoryService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.container = Container()
        self.history_service = self.container.history_service

    def test_get_history_returns_complete_history(self):
        """Test get_history returns complete history for an instruction."""
        # Create instruction through pipeline
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        history = self.container.history_service.get_history(result.instruction.id)

        assert isinstance(history, InstructionHistory)
        assert history.instruction.id == result.instruction.id
        assert len(history.versions) == 1
        assert history.versions[0].id == result.version.id
        assert history.variants_by_version[result.version.id][0].id == result.variant.id

    def test_get_latest_version_returns_newest(self):
        """Test get_latest_version returns the newest version."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        # Create second version
        version2 = self.container.history_service.create_new_version(
            instruction_id=result.instruction.id,
            change_summary="Added more content",
            created_by="test-user",
        )

        latest = self.container.history_service.get_latest_version(
            result.instruction.id
        )

        assert latest.id == version2.id
        assert latest.version_number == 2

    def test_create_multiple_versions(self):
        """Test creating multiple versions increments version number."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        v2 = self.container.history_service.create_new_version(
            instruction_id=result.instruction.id,
            change_summary="Second version",
            created_by="test-user",
        )

        v3 = self.container.history_service.create_new_version(
            instruction_id=result.instruction.id,
            change_summary="Third version",
            created_by="test-user",
        )

        assert v2.version_number == 2
        assert v3.version_number == 3
        assert v2.parent_version_id == result.version.id
        assert v3.parent_version_id == v2.id

        history = self.container.history_service.get_history(result.instruction.id)
        assert len(history.versions) == 3
        assert history.versions[0].version_number == 1
        assert history.versions[1].version_number == 2
        assert history.versions[2].version_number == 3

    def test_create_variant(self):
        """Test adding a variant to a version."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        variant = self.container.history_service.add_variant(
            version_id=result.version.id,
            variant_name="Experimental",
            description="Test variant",
        )

        assert variant.variant_name == "Experimental"
        assert variant.version_id == result.version.id
        assert variant.description == "Test variant"
        assert variant.parent_variant_id is None

        # Verify it's in history
        history = self.container.history_service.get_history(result.instruction.id)
        assert len(history.variants_by_version[result.version.id]) == 2

    def test_create_variant_with_parent(self):
        """Test adding a variant with a parent variant."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        # Add child variant
        child_variant = self.container.history_service.add_variant_with_parent(
            version_id=result.version.id,
            variant_name="Child Variant",
            description="Child of primary",
            parent_variant_id=result.variant.id,
        )

        assert child_variant.parent_variant_id == result.variant.id

        # Verify lineage in history
        history = self.container.history_service.get_history(result.instruction.id)
        variants = history.variants_by_version[result.version.id]
        assert len(variants) == 2
        root_variants = [v for v in variants if v.parent_variant_id is None]
        assert len(root_variants) == 1

    def test_version_lineage(self):
        """Test version lineage is preserved."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        self.container.history_service.create_new_version(
            instruction_id=result.instruction.id,
            change_summary="Second version",
            created_by="test-user",
        )

        self.container.history_service.create_new_version(
            instruction_id=result.instruction.id,
            change_summary="Third version",
            created_by="test-user",
        )

        history = self.container.history_service.get_history(result.instruction.id)

        assert history.versions[0].parent_version_id is None
        assert history.versions[1].parent_version_id == history.versions[0].id
        assert history.versions[2].parent_version_id == history.versions[1].id

    def test_repository_persistence(self):
        """Test that history persists across service calls."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        # Create history with same container
        history1 = self.container.history_service.get_history(result.instruction.id)
        assert len(history1.versions) == 1

        # Create new version
        self.container.history_service.create_new_version(
            instruction_id=result.instruction.id,
            change_summary="Second version",
            created_by="test-user",
        )

        # Get history again - should have 2 versions
        history2 = self.container.history_service.get_history(result.instruction.id)
        assert len(history2.versions) == 2

    def test_variant_persistence(self):
        """Test that variants persist across history calls."""
        pipeline = self.container.instruction_pipeline
        answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

        result = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        self.container.history_service.add_variant(
            version_id=result.version.id,
            variant_name="Experimental",
            description="Test variant",
        )

        history = self.container.history_service.get_history(result.instruction.id)
        variants = history.variants_by_version[result.version.id]
        assert len(variants) == 2

    def test_get_latest_version_no_versions_raises(self):
        """Test get_latest_version raises for instruction with no versions."""
        # Create instruction without versions
        instruction = Instruction(
            id="test-inst-no-versions",
            template_name="Test",
            context={},
            assembled_instruction="Test",
        )
        self.container.instruction_repository.save(instruction)

        with pytest.raises(ValueError, match="No versions found"):
            self.container.history_service.get_latest_version(instruction.id)

    def test_get_history_not_found_raises(self):
        """Test get_history raises for non-existent instruction."""
        with pytest.raises(ValueError):
            self.container.history_service.get_history("non-existent-id")
