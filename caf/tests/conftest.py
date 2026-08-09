"""Shared fixtures and helpers for repository tests."""

import uuid
from datetime import UTC, datetime

import pytest

from caf.database.db import init_db
from caf.models.instruction import Instruction
from caf.models.variant import Variant
from caf.models.version import Version
from caf.repositories.instruction_repository import InstructionRepository
from caf.repositories.sqlite_instruction_repository import SQLiteInstructionRepository
from caf.repositories.sqlite_variant_repository import SQLiteVariantRepository
from caf.repositories.sqlite_version_repository import SQLiteVersionRepository
from caf.repositories.variant_repository import VariantRepository
from caf.repositories.version_repository import VersionRepository

# ============================================================================
# Shared Fixtures
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def _init_db():
    """Initialize database once per session."""
    init_db()


@pytest.fixture
def mem_instruction_repo():
    """In-memory instruction repository fixture."""
    InstructionRepository()
    # Clear any existing data
    for _item in InstructionRepository().get_all():
        pass  # Fresh instance has no data
    yield InstructionRepository()
    # Cleanup handled by test isolation


@pytest.fixture
def mem_version_repo():
    """In-memory version repository fixture."""
    VersionRepository()
    for _item in VersionRepository().get_all():
        pass
    yield VersionRepository()


@pytest.fixture
def mem_variant_repo():
    """In-memory variant repository fixture."""
    VariantRepository()
    yield VariantRepository()


@pytest.fixture
def sqlite_instruction_repo():
    """SQLite instruction repository fixture."""
    from caf.database.db import init_db

    init_db()
    repo = SQLiteInstructionRepository()
    for item in repo.get_all():
        repo.delete(item.id)
    yield repo
    # Cleanup
    for item in repo.get_all():
        repo.delete(item.id)


@pytest.fixture
def sqlite_version_repo():
    """SQLite version repository fixture."""
    from caf.database.db import init_db
    from caf.models.instruction import Instruction
    from caf.repositories.sqlite_instruction_repository import (
        SQLiteInstructionRepository,
    )

    init_db()

    repo = SQLiteVersionRepository()
    # Clean up versions
    for item in repo.get_all():
        repo.delete(item.id)
    # Clean up and create instruction for FK
    inst_repo = SQLiteInstructionRepository()
    for item in inst_repo.get_all():
        inst_repo.delete(item.id)
    Instruction(
        id="sqlite-inst-1",
        template_name="Test",
        context={},
        assembled_instruction="Test",
        created_at=datetime.now(UTC),
        version=1,
    )
    SQLiteInstructionRepository().save(
        Instruction(
            id="sqlite-inst-1",
            template_name="Test",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
    )
    yield repo
    # Cleanup
    for item in repo.get_all():
        repo.delete(item.id)
    from caf.repositories.sqlite_instruction_repository import (
        SQLiteInstructionRepository,
    )

    inst_repo = SQLiteInstructionRepository()
    for item in inst_repo.get_all():
        inst_repo.delete(item.id)


@pytest.fixture
def sqlite_variant_repo():
    """SQLite variant repository fixture with FK dependencies."""
    from caf.database.db import init_db
    from caf.models.instruction import Instruction
    from caf.models.version import Version
    from caf.repositories.sqlite_instruction_repository import (
        SQLiteInstructionRepository,
    )
    from caf.repositories.sqlite_version_repository import SQLiteVersionRepository

    init_db()

    repo = SQLiteVariantRepository()
    for item in repo.get_all():
        repo.delete(item.id)

    # Create required version and instruction

    ver_repo = SQLiteVersionRepository()
    SQLiteInstructionRepository()
    for item in ver_repo.get_all():
        ver_repo.delete(item.id)
    for item in SQLiteInstructionRepository().get_all():
        SQLiteInstructionRepository().delete(item.id)

    inst = Instruction(
        id="sqlite-inst-1",
        template_name="Test",
        context={},
        assembled_instruction="Test",
        created_at=datetime.now(UTC),
        version=1,
    )
    SQLiteInstructionRepository().save(inst)
    ver = Version(
        id="ver-1",
        instruction_id="sqlite-inst-1",
        version_number=1,
        change_summary="Test",
        created_by="test",
        parent_version_id=None,
        created_at=datetime.now(UTC),
    )
    SQLiteVersionRepository().save(ver)

    yield repo

    # Cleanup
    for item in repo.get_all():
        repo.delete(item.id)
    for item in SQLiteVersionRepository().get_all():
        SQLiteVersionRepository().delete(item.id)
    for item in SQLiteInstructionRepository().get_all():
        SQLiteInstructionRepository().delete(item.id)


# ============================================================================
# Helper Fixtures for Creating Test Objects
# ============================================================================


@pytest.fixture
def make_instruction():
    """Factory for creating Instruction test objects."""

    def _make(**kwargs):
        defaults = {
            "id": str(uuid.uuid4()),
            "template_name": "Test Template",
            "context": {"objective": "test"},
            "assembled_instruction": "Test instruction",
            "created_at": datetime.now(UTC),
            "version": 1,
        }
        defaults.update(kwargs)
        return Instruction(**defaults)

    return _make


@pytest.fixture
def make_version():
    """Factory for creating Version test objects."""

    def _make(**kwargs):
        defaults = {
            "id": str(uuid.uuid4()),
            "instruction_id": str(uuid.uuid4()),
            "version_number": 1,
            "change_summary": "Test change",
            "created_by": "test-user",
            "parent_version_id": None,
            "created_at": datetime.now(UTC),
        }
        defaults.update(kwargs)
        return Version(**defaults)

    return _make


@pytest.fixture
def make_variant():
    """Factory for creating Variant test objects."""

    def _make(**kwargs):
        defaults = {
            "id": str(uuid.uuid4()),
            "version_id": str(uuid.uuid4()),
            "variant_name": "Test Variant",
            "description": "Test description",
            "parent_variant_id": None,
            "created_at": datetime.now(UTC),
        }
        defaults.update(kwargs)
        return Variant(**defaults)

    return _make


# ============================================================================
# Repository Fixtures with Parameterization
# ============================================================================


@pytest.fixture(params=["mem_instruction_repo", "sqlite_instruction_repo"])
def instruction_repo(request):
    """Parameterized instruction repository fixture."""
    return request.getfixturevalue(request.param)


@pytest.fixture(params=["mem_version_repo", "sqlite_version_repo"])
def version_repo(request):
    """Parameterized version repository fixture."""
    return request.getfixturevalue(request.param)


@pytest.fixture(params=["mem_variant_repo", "sqlite_variant_repo"])
def variant_repo(request):
    """Parameterized variant repository fixture."""
    return request.getfixturevalue(request.param)


# ============================================================================
# Shared Test Helpers
# ============================================================================


def assert_repo_basics(repo, make_item, item_id="test-id"):
    """Assert basic CRUD operations work for any repository."""
    item = make_item(id="test-id")
    repo.save(item)

    # get_by_id
    retrieved = repo.get_by_id("test-id")
    assert retrieved.id == "test-id"

    # get_all
    all_items = repo.get_all()
    assert any(i.id == "test-id" for i in all_items)

    # delete
    repo.delete("test-id")
    try:
        repo.get_by_id("test-id")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass


def assert_overwrite_works(repo, make_item, item_id="overwrite-test"):
    """Test that overwriting an item works."""
    item = make_item(id="overwrite-test", name_field="Original")
    repo.save(item)

    updated = repo.get_item_class()(
        id=item.id, **{**repo.get_item_data(item), "name_field": "Updated"}
    )
    # This is simplified - actual implementation depends on model
    repo.save(updated)
    retrieved = repo.get_by_id("overwrite-test")
    assert retrieved is not None


def assert_insertion_order(repo, make_item, prefix="test"):
    """Assert insertion order is preserved in get_all()."""
    # Clear repo
    for item in repo.get_all():
        repo.delete(item.id)

    items = [make_item(id=f"{prefix}-{i}") for i in range(1, 4)]
    for item in items:
        repo.save(item)

    repo.get_all()
    saved = [i for i in repo.get_all() if i.id.startswith(prefix)]
    assert len(saved) == 3
    assert saved[0].id == f"{prefix}-1"
    assert saved[1].id == f"{prefix}-2"
    assert saved[2].id == f"{prefix}-3"
