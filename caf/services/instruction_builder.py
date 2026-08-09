"""Instruction builder service for CAF application."""

import uuid
from typing import Any

from caf.models.instruction import Instruction
from caf.services.template_service import TemplateService
from caf.utils.placeholder_parser import PlaceholderParser


class InstructionBuilder:
    """Builds Instruction objects by assembling templates with context."""

    def __init__(self, template_service: TemplateService):
        """Initialize InstructionBuilder.

        Args:
            template_service: Template service instance.
        """
        self._template_service = template_service

    def build(self, template_id: str, context: Any) -> Instruction:
        """Build an Instruction from a template and context.

        Args:
            template_id: ID of the template to use.
            context: Context object with values for placeholders.

        Returns:
            Instruction: Assembled instruction object.

        Raises:
            ValueError: If template is not found.
        """
        template = self._template_service.get_by_id(template_id)
        context_dict = context.model_dump()
        assembled_text = PlaceholderParser.replace_placeholders(
            template.template_text, context_dict
        )

        return Instruction(
            id=str(uuid.uuid4()),
            template_name=template.name,
            context=context_dict,
            assembled_instruction=assembled_text,
        )


# Global instruction builder instance for backward compatibility
instruction_builder = InstructionBuilder(TemplateService())
