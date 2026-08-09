#!/usr/bin/env python
"""
Example: Business Analysis Workflow

This example demonstrates using CAF for business analysis tasks
with version control and variant management.
"""

from caf.core.container import Container
from caf.models.context import Context


def main():
    # Create container with in-memory repositories
    container: Container = Container()  # noqa: F823

    # Get services
    pipeline = container.instruction_pipeline

    # Business context
    Context(
        objective="Analyze Q4 2024 sales performance and recommend Q1 2025 strategy",
        audience="Executive leadership team",
        tone="Executive",
        constraints=[
            "< 2000 words",
            "Include data-driven insights",
            "Actionable recommendations",
        ],
        output_format="PDF Report",
        risk_level="Medium",
        language="English",
        word_limit=2000,
        purpose="Strategic Planning",
        business_type="E-commerce",
    )

    print("=== CAF Business Analysis Workflow ===\n")

    # Step 1: Create initial instruction
    print("Step 1: Creating initial analysis instruction...")
    result = pipeline.create_instruction(
        answers={
            "objective": "Analyze Q4 2024 sales performance and recommend Q1 2025 strategy",
            "audience": "Executive leadership team",
            "tone": "Executive",
            "constraints": [
                "< 2000 words",
                "Include data-driven insights",
                "Actionable recommendations",
            ],
            "output_format": "PDF Report",
            "risk_level": "Medium",
            "language": "English",
            "word_limit": 2000,
            "purpose": "Strategic Planning",
            "business_type": "E-commerce",
        },
        template_id="business-analysis",
        created_by="analyst-john",
        change_summary="Initial business analysis instruction",
        variant_name="Primary Analysis",
    )

    if not result.success:
        print(f"[ERROR] Pipeline failed: {result.error}")
        return

    variant_id = result.variant.id

    print(f"[OK] Instruction created: {result.instruction.id[:8]}")
    print(
        f"[OK] Version created: {result.version.version_number} ({result.version.id[:8]})"
    )
    print(f"[OK] Variant created: {result.variant.variant_name} ({variant_id[:8]})")

    # Step 2: Create a new version with updates
    print("\nStep 2: Creating updated version with new data...")
    version2 = container.version_service.create_version(
        instruction_id=result.instruction.id,
        change_summary="Added Q4 revenue breakdown by region",
        created_by="analyst-jane",
        parent_version=container.history_service.get_latest_version(
            result.instruction.id
        ),
    )
    print(f"[OK] Version {version2.version_number} created: {version2.id[:8]}")

    # Step 3: Create a variant for different audience
    print("\nStep 3: Creating variant for board presentation...")
    variant2 = container.variant_service.create_variant(
        version_id=version2.id,
        variant_name="Board Summary",
        description="Condensed version for board meeting",
        parent_variant=container.variant_repository.get_by_id(
            container.history_service.get_history(result.instruction.id)
            .variants_by_version[result.version.id][0]
            .id
        ),
    )
    print(f"[OK] Variant created: {variant2.variant_name} ({variant2.id[:8]})")

    # Step 4: View history
    print("\nStep 4: Viewing complete history...")
    history = container.history_service.get_history(result.instruction.id)
    print(f"  Instruction: {history.instruction.template_name}")
    print(f"  Versions: {len(history.versions)}")
    for v in history.versions:
        print(f"  - v{v.version_number}: {v.change_summary}")
    for _ver_id, variants in history.variants_by_version.items():
        for v in variants:
            print(
                f"    - Variant: {v.variant_name} (parent: {v.parent_variant_id or 'None'})"
            )

    # Step 5: Compare versions
    print("\nStep 5: Comparing versions...")
    versions = container.history_service.get_history(result.instruction.id).versions
    if len(versions) >= 2:
        diff = container.diff_service.compare_versions(versions[0].id, versions[1].id)
        print(f"  Similarity: {diff.similarity_score:.1f}%")
        print(f"  Added lines: {len(diff.added_lines)}")
        print(f"  Removed lines: {len(diff.removed_lines)}")
        print(f"  Changed lines: {len(diff.changed_lines)}")

    # Step 6: Export/Import
    print("\nStep 6: Export/Import demonstration...")

    json_str = container.export_import_service.export_json(result.instruction.id)
    print(f"  Exported JSON length: {len(json_str)} chars")

    # Create new container and import
    from caf.core.container import Container

    new_container = Container(use_sqlite=False)
    imported = new_container.export_import_service.import_json(json_str)
    print(f"  Imported: {imported.instruction.template_name}")
    print(f"  Versions: {len(imported.versions)}")
    print(f"  Variants: {len(imported.variants)}")

    print("\n" + "=" * 60)
    print("[OK] All workflow steps completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
