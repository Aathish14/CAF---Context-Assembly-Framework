"""End-to-end integration test for CAF complete pipeline."""

from datetime import datetime
from uuid import UUID

from caf.models.context import Context
from caf.models.instruction import Instruction
from caf.models.variant import Variant
from caf.models.version import Version
from caf.repositories.instruction_repository import InstructionRepository
from caf.repositories.variant_repository import VariantRepository
from caf.repositories.version_repository import VersionRepository
from caf.services.context_builder import ContextBuilder
from caf.services.instruction_builder import InstructionBuilder
from caf.services.question_service import question_service
from caf.services.template_service import TemplateService
from caf.services.validation_service import validation_service
from caf.services.variant_service import VariantService
from caf.services.version_service import VersionService


class TestEndToEndPipeline:
    """Integration test covering the complete CAF pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        self.context_builder = ContextBuilder()
        # Use answers matching the actual questions from question_service
        self.valid_answers = {
            "objective": "Write a technical blog post",
            "audience": "Software Engineers",
            "tone": "Technical",
            "constraints": "< 1500 words, Include code examples",  # String for text question
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": "1500",  # String for text question
            "purpose": "Educate",  # Fixed: was "Education", now matches option "Educate"
            "business_type": "SaaS",
        }
        # Separate answers for ContextBuilder (will be converted to proper types)
        self.context_answers = {
            "objective": "Write a technical blog post",
            "audience": "Software Engineers",
            "tone": "Technical",
            "constraints": "< 1500 words, Include code examples",  # String from text question
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": "1500",  # String from text question
            "purpose": "Educate",  # Fixed: was "Education", now matches option "Educate"
            "business_type": "SaaS",
        }
        # Create repositories
        self.instruction_repo = InstructionRepository()
        self.version_repo = VersionRepository()
        self.variant_repo = VariantRepository()

        # Create services with in-memory repositories
        self.template_service = TemplateService()
        self.instruction_builder = InstructionBuilder(
            template_service=self.template_service
        )
        self.version_service = VersionService(version_repository=self.version_repo)
        self.variant_service = VariantService(variant_repository=self.variant_repo)

    def test_complete_pipeline(self):
        """Test the complete CAF workflow end-to-end."""

        # 1. Questions are loaded successfully
        questions = question_service.get_all_questions()
        assert len(questions) > 0
        assert all("id" in q and "type" in q for q in questions)

        # 2. Validation succeeds for valid answers
        validation_results = validation_service.validate_all(
            questions, self.valid_answers
        )
        assert all(result.is_valid for result in validation_results.values())

        # 3. ContextBuilder creates a valid Context
        context = self.context_builder.build(self.context_answers)
        assert isinstance(context, Context)
        assert context.objective == "Write a technical blog post"
        assert context.audience == "Software Engineers"
        assert context.tone == "Technical"
        assert context.constraints == ["< 1500 words", "Include code examples"]

        # 4. TemplateService loads templates
        templates = self.template_service.get_all()
        assert len(templates) == 3
        template_names = {t.name for t in templates}
        assert template_names == {
            "General Prompt",
            "Business Analysis",
            "Software Engineering",
        }

        # 5. InstructionBuilder assembles an Instruction
        instruction = self.instruction_builder.build("general-prompt", context)
        assert isinstance(instruction, Instruction)
        assert instruction.template_name == "General Prompt"
        assert instruction.version == 1
        assert len(instruction.id) > 0
        assert isinstance(instruction.created_at, datetime)
        assert instruction.created_at.tzinfo is not None  # timezone-aware

        # 6. InstructionRepository persists the Instruction
        self.instruction_repo.save(instruction)

        # 7. Retrieved Instruction matches the saved object
        retrieved = self.instruction_repo.get_by_id(instruction.id)
        assert retrieved.id == instruction.id
        assert retrieved.template_name == instruction.template_name
        assert retrieved.assembled_instruction == instruction.assembled_instruction
        assert retrieved.context == instruction.context

        # 8. VersionService creates Version 1
        version1 = self.version_service.create_version(
            instruction_id=instruction.id,
            change_summary="Initial version",
            created_by="test-user",
        )
        assert isinstance(version1, Version)
        assert version1.version_number == 1
        assert version1.instruction_id == instruction.id
        assert version1.parent_version_id is None
        assert version1.change_summary == "Initial version"
        assert version1.created_by == "test-user"
        assert isinstance(version1.created_at, datetime)
        assert version1.created_at.tzinfo is not None  # timezone-aware

        # 9. VersionRepository persists it
        self.version_repo.save(version1)
        retrieved_version = self.version_repo.get_by_id(version1.id)
        assert retrieved_version.id == version1.id
        assert retrieved_version.version_number == 1

        # 10. Version 2 correctly references Version 1
        version2 = self.version_service.create_version(
            instruction_id=instruction.id,
            change_summary="Added more examples",
            created_by="test-user",
            parent_version=version1,
        )
        assert version2.version_number == 2
        assert version2.parent_version_id == version1.id
        assert version2.instruction_id == instruction.id

        # Verify both versions exist for this instruction
        versions = self.version_repo.get_by_instruction_id(instruction.id)
        assert len(versions) == 2
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2

        # 11. VariantService creates a root Variant
        variant1 = self.variant_service.create_variant(
            version_id=version1.id,
            variant_name="Primary Variant",
            description="Main variant for production",
        )
        assert isinstance(variant1, Variant)
        assert variant1.variant_name == "Primary Variant"
        assert variant1.version_id == version1.id
        assert variant1.parent_variant_id is None
        assert variant1.description == "Main variant for production"
        assert isinstance(variant1.created_at, datetime)
        assert variant1.created_at.tzinfo is not None  # timezone-aware

        # 12. VariantService creates a child Variant
        variant2 = self.variant_service.create_variant(
            version_id=version1.id,
            variant_name="Experimental Variant",
            description="Test variant",
            parent_variant=variant1,
        )
        assert variant2.variant_name == "Experimental Variant"
        assert variant2.parent_variant_id == variant1.id
        assert variant2.version_id == version1.id

        # 13. VariantRepository preserves lineage
        self.variant_repo.save(variant1)
        self.variant_repo.save(variant2)
        retrieved_variant = self.variant_repo.get_by_id(variant1.id)
        assert retrieved_variant.id == variant1.id
        assert retrieved_variant.variant_name == "Primary Variant"

        child_variants = self.variant_repo.get_by_version_id(version1.id)
        assert len(child_variants) == 2
        root_variants = [v for v in child_variants if v.parent_variant_id is None]
        assert len(root_variants) == 1
        assert root_variants[0].id == variant1.id

        # 14. UUIDs are unique
        all_ids = [
            instruction.id,
            version1.id,
            version2.id,
            variant1.id,
            variant2.id,
        ]
        assert len(set(all_ids)) == len(all_ids)
        # Verify each is a valid UUID
        for uid in all_ids:
            UUID(uid)  # Should not raise

        # 15. created_at fields are timezone-aware
        for obj in [instruction, version1, version2, variant1, variant2]:
            assert obj.created_at.tzinfo is not None
            assert obj.created_at.tzinfo.utcoffset(obj.created_at) is not None

        # 16. Entire pipeline completes without exceptions
        # If we reach here, all steps passed
        assert True
