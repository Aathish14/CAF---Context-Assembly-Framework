#!/usr/bin/env python
"""
Example: Basic Instruction Generation

This example demonstrates the basic usage of CAF to generate instructions
from templates using context.
"""

from caf.models.context import Context
from caf.services.instruction_builder import instruction_builder
from caf.services.template_service import template_service


def main():
    # Create context with all required fields
    context = Context(
        objective="Write a technical blog post about Python async programming",
        audience="Python developers",
        tone="Technical",
        constraints=["< 1500 words", "Include code examples", "Explain async/await"],
        output_format="Markdown",
        risk_level="Low",
        language="English",
        word_limit=1500,
        purpose="Education",
        business_type="SaaS",
    )

    # List available templates
    print("Available templates:")
    for template in template_service.get_all():
        print(f"  - {template.id}: {template.name} ({template.category})")

    # Build instruction using general-prompt template
    instruction = instruction_builder.build("general-prompt", context)

    print("\n" + "=" * 60)
    print("GENERATED INSTRUCTION")
    print("=" * 60)
    print(f"Template: {instruction.template_name}")
    print(f"Version: {instruction.version}")
    print(f"ID: {instruction.id}")
    print(f"Created: {instruction.created_at}")
    print("-" * 60)
    print(instruction.assembled_instruction)
    print("=" * 60)

    print("\n✓ Instruction generated successfully!")


if __name__ == "__main__":
    main()
