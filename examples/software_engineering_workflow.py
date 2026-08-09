#!/usr/bin/env python
"""
Example: Software Engineering Task with Version Control

This example demonstrates using CAF for software engineering tasks
with full version control and diff capabilities.
"""

from caf.core.container import Container
from caf.models.context import Context


def main():
    container = Container()

    Context(
        objective="Design a REST API for a user management system",
        audience="Backend developers",
        tone="Technical",
        constraints=[
            "Follow REST conventions",
            "Use OpenAPI 3.0 specification",
            "Include error handling patterns",
            "Add pagination for list endpoints",
            "Include rate limiting considerations",
        ],
        output_format="OpenAPI 3.0 YAML",
        risk_level="Low",
        language="Python (FastAPI)",
        word_limit=2000,
        purpose="API Design",
        business_type="SaaS Platform",
    )

    print("=== CAF Software Engineering Workflow ===\n")

    # Create initial API design instruction
    result = container.instruction_pipeline.create_instruction(
        answers={
            "objective": "Design a REST API for user management",
            "audience": "Backend developers",
            "tone": "Technical",
            "constraints": [
                "Follow REST conventions",
                "Use OpenAPI 3.0",
                "Include error handling",
                "Add pagination",
                "Rate limiting",
            ],
            "output_format": "OpenAPI 3.0 YAML",
            "risk_level": "Low",
            "language": "Python (FastAPI)",
            "word_limit": 2000,
            "purpose": "API Design",
            "business_type": "SaaS Platform",
        },
        template_id="software-engineering",
        created_by="api-team-lead",
        change_summary="Initial API design specification",
        variant_name="v1-initial-design",
    )

    if not result.success:
        print(f"❌ Failed: {result.error}")
        return

    instruction = result.instruction
    version1 = result.version
    variant1 = result.variant

    print(f"✓ Created: {instruction.template_name}")
    print(f"  Instruction: {instruction.id[:8]}")
    print(f"  Version: v{version1.version_number} ({version1.id[:8]})")
    print(f"  Variant: {variant1.variant_name} ({variant1.id[:8]})")

    # Create version 2 with authentication
    print("\n--- Creating v2: Added Authentication ---")
    version2 = container.version_service.create_version(
        instruction_id=result.instruction.id,
        change_summary="Added JWT authentication and OAuth2 flows",
        created_by="api-team-lead",
        parent_version=container.history_service.get_latest_version(
            result.instruction.id
        ),
    )
    print(f"✓ Version {version2.version_number} created: {version2.id[:8]}")

    # Create variant for mobile team
    print("\n--- Creating mobile team variant ---")
    variant2 = container.variant_service.create_variant(
        version_id=version2.id,
        variant_name="Mobile Team Variant",
        description="Simplified endpoints for mobile clients",
        parent_variant=container.variant_repository.get_by_id(
            container.history_service.get_history(result.instruction.id)
            .variants_by_version[version1.id][0]
            .id
        ),
    )
    print(f"✓ Variant: {variant2.variant_name}")

    # Create version 3 with rate limiting
    print("\n--- Creating v3: Rate Limiting & Caching ---")
    version3 = container.version_service.create_version(
        instruction_id=result.instruction.id,
        change_summary="Added rate limiting, caching headers, and request validation",
        created_by="api-team-lead",
        parent_version=container.history_service.get_latest_version(
            result.instruction.id
        ),
    )
    print(f"✓ Version {version3.version_number} created")

    # Compare v1 vs v3
    print("\n--- Comparing v1 vs v3 ---")
    diff = container.diff_service.compare_versions(
        container.history_service.get_history(result.instruction.id).versions[0].id,
        container.history_service.get_latest_version(result.instruction.id).id,
    )
    print(f"Similarity: {diff.similarity_score:.1f}%")
    print(f"Added: {len(diff.added_lines)} lines")
    print(f"Removed: {len(diff.removed_lines)} lines")
    print(f"Changed: {len(diff.changed_lines)} lines")
    print(f"Unified diff preview:\n{diff.unified_diff[:500]}...")

    # Show version chain
    print("\n--- Version Chain ---")
    chain = container.diff_service.get_version_chain(result.instruction.id)
    for i, d in enumerate(chain, 1):
        print(
            f"  {i}. v{d.old_version.version_number} -> v{d.new_version.version_number} ({d.similarity_score:.1f}% similar)"
        )

    # Full history
    print("\n--- Full History ---")
    history = container.history_service.get_history(result.instruction.id)
    print(f"Instruction: {history.instruction.template_name}")
    print(f"Total versions: {len(history.versions)}")
    for v in history.versions:
        variants = len(history.variants_by_version.get(v.id, []))
        print(f"  v{v.version_number}: {v.change_summary} ({variants} variants)")

    print("\n" + "=" * 60)
    print("✓ Software engineering workflow complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
