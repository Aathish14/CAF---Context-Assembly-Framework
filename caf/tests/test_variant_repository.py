"""Tests for VariantRepository (in-memory and SQLite)."""

import uuid
from datetime import UTC, datetime

import pytest

from caf.models.instruction import Instruction
from caf.models.variant import Variant
from caf.models.version import Version
from caf.repositories.sqlite_variant_repository import SQLiteVariantRepository
from caf.repositories.variant_repository import VariantRepository

# ============================================================================
# Shared Helper Factory
# ============================================================================


def make_variant(**kwargs):
    """Create a test Variant."""
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


# ============================================================================
# Parameterized Tests for Both Repository Types
# ============================================================================


class TestVariantRepository:
    """Tests for in-memory VariantRepository."""

    @pytest.fixture(autouse=True)
    def setup_repo(self):
        """Set up test fixtures."""
        self.repo = VariantRepository()
        for item in self.repo.get_all():
            self.repo.delete(item.id)

    def make_variant(self, **kwargs):
        """Create a test Variant."""
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

    def test_save(self):
        """Test saving a variant."""
        variant = self.make_variant()
        self.repo.save(variant)

        retrieved = self.repo.get_by_id(variant.id)
        assert retrieved.id == variant.id
        assert retrieved.version_id == variant.version_id
        assert retrieved.variant_name == "Test Variant"
        assert retrieved.description == "Test description"
        assert retrieved.parent_variant_id is None

    def test_get_by_id(self):
        """Test retrieving a variant by ID."""
        variant = self.make_variant(id="test-id-1")
        self.repo.save(variant)

        retrieved = self.repo.get_by_id("test-id-1")
        assert retrieved.id == "test-id-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all variants."""
        for i in range(3):
            v = self.make_variant(id=f"var-{i}")
            self.repo.save(v)

        self.repo.get_all()
        assert len([i for i in self.repo.get_all() if i.id.startswith("var-")]) == 3

    def test_delete(self):
        """Test deleting a variant."""
        variant = self.make_variant(id="test-delete")
        self.repo.save(variant)

        # Verify it exists
        assert self.repo.get_by_id(variant.id) is not None

        # Delete
        self.repo.delete(variant.id)

        # Verify it's gone
        with pytest.raises(ValueError):
            self.repo.get_by_id(variant.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing variant."""
        variant = self.make_variant(id="overwrite-test", variant_name="Original")
        self.repo.save(variant)

        updated = Variant(
            id=variant.id,
            version_id=variant.version_id,
            variant_name="Updated",
            description=variant.description,
            parent_variant_id=variant.parent_variant_id,
            created_at=variant.created_at,
        )
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(variant.id)
        assert retrieved.variant_name == "Updated"

    def test_get_by_version_id(self):
        """Test retrieving variants by version ID."""
        version_id = str(uuid.uuid4())

        v1 = self.make_variant(version_id=version_id, variant_name="Variant 1")
        v2 = self.make_variant(version_id=version_id, variant_name="Variant 2")
        v3 = self.make_variant(version_id=version_id, variant_name="Variant 3")

        self.repo.save(v1)
        self.repo.save(v2)
        self.repo.save(v3)

        variants = self.repo.get_by_version_id(version_id)
        assert len(variants) == 3
        assert {v.variant_name for v in variants} == {
            "Variant 1",
            "Variant 2",
            "Variant 3",
        }

    def test_parent_variant_id_preserved(self):
        """Test parent_variant_id is preserved."""
        parent_id = str(uuid.uuid4())
        child = self.make_variant(parent_variant_id=parent_id)
        self.repo.save(child)

        retrieved = self.repo.get_by_id(child.id)
        assert retrieved.parent_variant_id == parent_id

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        for item in self.repo.get_all():
            self.repo.delete(item.id)

        items = [
            self.make_variant(id="var-1"),
            self.make_variant(id="var-2"),
            self.make_variant(id="var-3"),
        ]

        for item in items:
            self.repo.save(item)

        all_items = self.repo.get_all()
        saved = [i for i in all_items if i.id.startswith("var-")]
        assert len(saved) == 3
        assert saved[0].id == "var-1"
        assert saved[1].id == "var-2"
        assert saved[2].id == "var-3"


class TestSQLiteVariantRepository:
    """Tests for SQLite VariantRepository."""

    @pytest.fixture(autouse=True)
    def setup_repo(self):
        """Set up test fixtures."""
        from caf.database.db import init_db

        init_db()
        self.repo = SQLiteVariantRepository()
        for item in self.repo.get_all():
            self.repo.delete(item.id)
        # Also clear versions and instructions to avoid FK conflicts
        from caf.repositories.sqlite_instruction_repository import (
            SQLiteInstructionRepository,
        )
        from caf.repositories.sqlite_version_repository import SQLiteVersionRepository

        ver_repo = SQLiteVersionRepository()
        inst_repo = SQLiteInstructionRepository()
        for item in ver_repo.get_all():
            ver_repo.delete(item.id)
        for item in inst_repo.get_all():
            inst_repo.delete(item.id)
        # Create a version and instruction for tests

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

    def teardown_method(self):
        """Clean up after tests."""
        for item in self.repo.get_all():
            self.repo.delete(item.id)
        from caf.repositories.sqlite_instruction_repository import (
            SQLiteInstructionRepository,
        )
        from caf.repositories.sqlite_version_repository import SQLiteVersionRepository

        ver_repo = SQLiteVersionRepository()
        inst_repo = SQLiteInstructionRepository()
        for item in ver_repo.get_all():
            ver_repo.delete(item.id)
        for item in inst_repo.get_all():
            inst_repo.delete(item.id)

    def test_save(self):
        """Test saving a variant."""
        variant = Variant(
            id="sqlite-var-1",
            version_id="ver-1",
            variant_name="SQLite Variant",
            description="Test description",
            parent_variant_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(variant)

        retrieved = self.repo.get_by_id(variant.id)
        assert retrieved.id == variant.id
        assert retrieved.variant_name == "SQLite Variant"

    def test_get_by_id(self):
        """Test retrieving a variant by ID."""
        variant = Variant(
            id="sqlite-test-1",
            version_id="ver-1",
            variant_name="SQLite Variant",
            description="Test",
            parent_variant_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(variant)

        retrieved = self.repo.get_by_id("sqlite-test-1")
        assert retrieved.id == "sqlite-test-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all variants."""
        for i in range(3):
            v = Variant(
                id=f"sqlite-var-{i}",
                version_id="ver-1",
                variant_name=f"Variant {i}",
                description="Test",
                parent_variant_id=None,
                created_at=datetime.now(UTC),
            )
            self.repo.save(v)

        assert len([i for i in self.repo.get_all() if i.id.startswith("sqlite-")]) == 3

    def test_delete(self):
        """Test deleting a variant."""
        variant = Variant(
            id="sqlite-delete",
            version_id="ver-1",
            variant_name="Test",
            description="Test",
            parent_variant_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(variant)

        assert self.repo.get_by_id(variant.id) is not None
        self.repo.delete(variant.id)

        with pytest.raises(ValueError):
            self.repo.get_by_id(variant.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing variant."""
        variant = Variant(
            id="sqlite-overwrite",
            version_id="ver-1",
            variant_name="Original",
            description="Test",
            parent_variant_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(variant)

        updated = Variant(
            id=variant.id,
            version_id=variant.version_id,
            variant_name="Updated",
            description=variant.description,
            parent_variant_id=variant.parent_variant_id,
            created_at=variant.created_at,
        )
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(variant.id)
        assert retrieved.variant_name == "Updated"

    def test_get_by_version_id(self):
        """Test retrieving variants by version ID."""
        version_id = "ver-1"

        for i in range(3):
            v = Variant(
                id=f"sqlite-v-{i}",
                version_id=version_id,
                variant_name=f"Variant {i}",
                description="Test",
                parent_variant_id=None,
                created_at=datetime.now(UTC),
            )
            self.repo.save(v)

        variants = self.repo.get_by_version_id(version_id)
        assert len(variants) == 3
        assert {v.variant_name for v in variants} == {
            "Variant 0",
            "Variant 1",
            "Variant 2",
        }

    def test_parent_variant_id_preserved(self):
        """Test parent_variant_id is preserved."""
        # First create the parent variant
        parent = Variant(
            id="sqlite-parent-1",
            version_id="ver-1",
            variant_name="Parent",
            description="Parent variant",
            parent_variant_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(parent)

        parent_id = "sqlite-parent-1"
        child = Variant(
            id="sqlite-child",
            version_id="ver-1",
            variant_name="Child",
            description="Test",
            parent_variant_id=parent_id,
            created_at=datetime.now(UTC),
        )
        self.repo.save(child)

        retrieved = self.repo.get_by_id(child.id)
        assert retrieved.parent_variant_id == parent_id

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        for item in self.repo.get_all():
            self.repo.delete(item.id)

        items = [
            Variant(
                id=f"order-{i}",
                version_id="ver-1",
                variant_name=f"Var {i}",
                description="",
                parent_variant_id=None,
                created_at=datetime.now(UTC),
            )
            for i in range(1, 4)
        ]

        for item in items:
            self.repo.save(item)

        all_items = self.repo.get_all()
        saved = [i for i in all_items if i.id.startswith("order-")]
        assert len(saved) == 3
        assert saved[0].id == "order-1"
        assert saved[1].id == "order-2"
        assert saved[2].id == "order-3"
