"""Integration test for instruction pipeline."""

from caf.core.container import Container
from caf.models.pipeline_result import PipelineResult


class TestInstructionPipeline:
    """Integration tests for the instruction pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        self.container = Container()

    def test_complete_pipeline_success(self):
        """Test the complete pipeline from answers to variant."""
        pipeline = self.container.instruction_pipeline

        answers = {
            "objective": "Write a technical blog post",
            "audience": "Software Engineers",
            "tone": "Technical",
            "constraints": ["< 1500 words", "Include code examples"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1500,
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

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.error is None

        # Verify instruction
        assert result.instruction is not None
        assert result.instruction.template_name == "General Prompt"
        assert result.instruction.version == 1
        assert result.instruction.id is not None

        # Verify version
        assert result.version is not None
        assert result.version.version_number == 1
        assert result.version.instruction_id == result.instruction.id
        assert result.version.parent_version_id is None
        assert result.version.change_summary == "Initial version"
        assert result.version.created_by == "test-user"

        # Verify variant
        assert result.variant is not None
        assert result.variant.variant_name == "Primary"
        assert result.variant.version_id == result.version.id
        assert result.variant.parent_variant_id is None

    def test_pipeline_with_different_variant_name(self):
        """Test pipeline with custom variant name."""
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
            variant_name="Custom Variant",
        )

        assert result.success is True
        assert result.variant.variant_name == "Custom Variant"

    def test_pipeline_with_all_templates(self):
        """Test pipeline works with all available templates."""
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

        for template_id in [
            "general-prompt",
            "business-analysis",
            "software-engineering",
        ]:
            result = pipeline.create_instruction(
                answers=answers,
                template_id=template_id,
                created_by="test-user",
                change_summary="Initial version",
                variant_name="Primary",
            )
            assert result.success is True
            assert result.instruction.template_name in [
                "General Prompt",
                "Business Analysis",
                "Software Engineering",
            ]

    def test_pipeline_creates_unique_ids(self):
        """Test that pipeline creates unique IDs for each run."""
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

        result1 = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        result2 = pipeline.create_instruction(
            answers=answers,
            template_id="general-prompt",
            created_by="test-user",
            change_summary="Initial version",
            variant_name="Primary",
        )

        assert result1.success is True
        assert result2.success is True
        assert result1.instruction.id != result2.instruction.id
        assert result1.version.id != result2.version.id
        assert result1.variant.id != result2.variant.id

    def test_pipeline_uses_container_services(self):
        """Test that pipeline uses services from container."""
        # Create a fresh container
        container = Container()
        pipeline = container.instruction_pipeline

        # Verify all services are from the same container
        assert pipeline._validation_service is container.validation_service
        assert pipeline._context_builder is container.context_builder
        assert pipeline._instruction_builder is container.instruction_builder
        assert pipeline._version_service is container.version_service
        assert pipeline._variant_service is container.variant_service
        assert pipeline._instruction_repository is container.instruction_repository
        assert pipeline._version_repository is container.version_repository
        assert pipeline._variant_repository is container.variant_repository

    def test_pipeline_with_sqlite_container(self):
        """Test pipeline works with SQLite container."""
        container = Container(use_sqlite=True)
        pipeline = container.instruction_pipeline

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

        assert result.success is True
        assert result.instruction is not None
        assert result.version is not None
        assert result.variant is not None
