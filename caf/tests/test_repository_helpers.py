"""Shared test helpers for repository tests."""

import uuid
from datetime import UTC, datetime
from typing import TypeVar

from caf.repositories.base_repository import BaseRepository

T = TypeVar("T")


def create_test_item[T](_model_class: type[T], **kwargs) -> T:
    """Create a test item with defaults."""
    if "id" not in kwargs:
        kwargs["id"] = str(uuid.uuid4())
    return kwargs


def verify_basic_crud(repository: BaseRepository, item_factory, **item_kwargs):
    """Verify basic CRUD operations for a repository."""
    # Create
    item = item_factory(**item_kwargs)
    repository.save(item)

    # Read by ID
    retrieved = repository.get_by_id(item.id)
    assert retrieved.id == item.id

    # Get all
    all_items = repository.get_all()
    assert len(all_items) >= 1
    assert any(i.id == item.id for i in all_items)

    # Update (overwrite)
    item_copy = item_factory(
        id=item.id, **{k: v for k, v in item_kwargs.items() if k != "id"}
    )
    repository.save(item_copy)
    retrieved = repository.get_by_id(item.id)
    assert retrieved.id == item.id

    # Delete
    repository.delete(item.id)
    try:
        repository.get_by_id(item.id)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass


def verify_insertion_order(repository: BaseRepository, item_factory, items_data: list):
    """Verify insertion order is preserved in get_all()."""
    repository.reset() if hasattr(repository, "reset") else None

    items = []
    for data in items_data:
        item = item_factory(**data)
        repository.save(item)
        items.append(item)

    all_items = repository.get_all()
    saved_items = [i for i in all_items if i.id in [item.id for item in items]]
    assert len(saved_items) == len(items)

    # Check order matches insertion order
    for i, item in enumerate(saved_items):
        assert item.id == items[i].id


def verify_repository_specific(
    repository: BaseRepository, item_factory, test_specific_func
):
    """Run repository-specific tests."""
    test_specific_func(repository, item_factory)


def make_instruction(**kwargs):
    """Create a test Instruction."""
    from caf.models.instruction import Instruction

    defaults = {
        "template_name": "Test Template",
        "context": {"objective": "test"},
        "assembled_instruction": "Test instruction",
        "version": 1,
    }
    defaults.update(kwargs)
    if "id" not in defaults:
        defaults["id"] = str(uuid.uuid4())
    if "created_at" not in defaults:
        defaults["created_at"] = datetime.now(UTC)
    return Instruction(**defaults)


def make_version(**kwargs):
    """Create a test Version."""
    from caf.models.version import Version

    defaults = {
        "instruction_id": str(uuid.uuid4()),
        "version_number": 1,
        "change_summary": "Test change",
        "created_by": "test-user",
        "parent_version_id": None,
    }
    defaults.update(kwargs)
    if "id" not in defaults:
        defaults["id"] = str(uuid.uuid4())
    if "created_at" not in defaults:
        defaults["created_at"] = datetime.now(UTC)
    return Version(**defaults)


def make_variant(**kwargs):
    """Create a test Variant."""
    from caf.models.variant import Variant

    defaults = {
        "version_id": str(uuid.uuid4()),
        "variant_name": "Test Variant",
        "description": "Test description",
        "parent_variant_id": None,
    }
    defaults.update(kwargs)
    if "id" not in defaults:
        defaults["id"] = str(uuid.uuid4())
    if "created_at" not in defaults:
        defaults["created_at"] = datetime.now(UTC)
    return Variant(**defaults)
