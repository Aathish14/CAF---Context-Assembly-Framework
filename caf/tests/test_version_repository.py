"""Tests for VersionRepository (in-memory and SQLite)."""

import uuid
from datetime import UTC, datetime

import pytest

from caf.models.instruction import Instruction
from caf.models.version import Version
from caf.repositories.sqlite_instruction_repository import SQLiteInstructionRepository
from caf.repositories.sqlite_version_repository import SQLiteVersionRepository
from caf.repositories.version_repository import VersionRepository

# ============================================================================
# Shared Helper Factory
# ============================================================================


def make_version(**kwargs):
    """Create a test Version."""
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


# ============================================================================
# Parameterized Tests for Both Repository Types
# ============================================================================


class TestVersionRepository:
    """Tests for in-memory VersionRepository."""

    @pytest.fixture(autouse=True)
    def setup_repo(self):
        """Set up test fixtures."""
        self.repo = VersionRepository()
        for item in self.repo.get_all():
            self.repo.delete(item.id)

    def make_version(self, **kwargs):
        """Create a test Version."""
        defaults = {
            "id": str(uuid.uuid4()),
            "instruction_id": str(uuid.uuid4()),
            "version_number": 1,
            "change_summary": "Test change",
            "created_by": "test-user",
            "parent_version_id": None,
            "created_at": datetime.now(UTC),
        }
        return Version(**{**defaults, **kwargs})

    def test_save(self):
        """Test saving a version."""
        version = self.make_version()
        self.repo.save(version)

        retrieved = self.repo.get_by_id(version.id)
        assert retrieved.id == version.id
        assert retrieved.instruction_id == version.instruction_id
        assert retrieved.version_number == 1
        assert retrieved.change_summary == "Test change"
        assert retrieved.created_by == "test-user"
        assert retrieved.parent_version_id is None

    def test_get_by_id(self):
        """Test retrieving a version by ID."""
        version = make_version(id="test-id-1")
        self.repo.save(version)

        retrieved = self.repo.get_by_id("test-id-1")
        assert retrieved.id == "test-id-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all versions."""
        for i in range(3):
            v = self.make_version(id=f"ver-{i}")
            self.repo.save(v)

        self.repo.get_all()
        assert len([i for i in self.repo.get_all() if i.id.startswith("ver-")]) == 3

    def test_delete(self):
        """Test deleting a version."""
        version = self.make_version(id="test-delete")
        self.repo.save(version)

        # Verify it exists
        assert self.repo.get_by_id(version.id) is not None

        # Delete
        self.repo.delete(version.id)

        # Verify it's gone
        with pytest.raises(ValueError):
            self.repo.get_by_id(version.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing version."""
        version = self.make_version(id="overwrite-test", change_summary="Original")
        self.repo.save(version)

        updated = self.make_version(id=version.id, change_summary="Updated")
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(version.id)
        assert retrieved.change_summary == "Updated"

    def test_get_by_instruction_id(self):
        """Test retrieving versions by instruction ID."""
        instruction_id = str(uuid.uuid4())

        v1 = self.make_version(instruction_id=instruction_id, version_number=1)
        v2 = self.make_version(instruction_id=instruction_id, version_number=2)
        v3 = self.make_version(instruction_id=instruction_id, version_number=3)

        self.repo.save(v1)
        self.repo.save(v2)
        self.repo.save(v3)

        versions = self.repo.get_by_instruction_id(instruction_id)
        assert len(versions) == 3
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2
        assert versions[2].version_number == 3

    def test_version_ordering(self):
        """Test versions are ordered by version_number."""
        instruction_id = str(uuid.uuid4())

        v2 = self.make_version(instruction_id=instruction_id, version_number=2)
        v1 = self.make_version(instruction_id=instruction_id, version_number=1)
        v3 = self.make_version(instruction_id=instruction_id, version_number=3)

        self.repo.save(v2)
        self.repo.save(v1)
        self.repo.save(v3)

        versions = self.repo.get_by_instruction_id(instruction_id)
        assert len(versions) == 3
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2
        assert versions[2].version_number == 3

    def test_parent_version_id_preserved(self):
        """Test parent_version_id is preserved."""
        parent_id = str(uuid.uuid4())
        child = self.make_version(parent_version_id=parent_id)
        self.repo.save(child)

        retrieved = self.repo.get_by_id(child.id)
        assert retrieved.parent_version_id == parent_id

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        for item in self.repo.get_all():
            self.repo.delete(item.id)

        items = [
            self.make_version(id="ver-1"),
            self.make_version(id="ver-2"),
            self.make_version(id="ver-3"),
        ]

        for item in items:
            self.repo.save(item)

        all_items = self.repo.get_all()
        saved = [i for i in all_items if i.id.startswith("ver-")]
        assert len(saved) == 3
        assert saved[0].id == "ver-1"
        assert saved[1].id == "ver-2"
        assert saved[2].id == "ver-3"


class TestSQLiteVersionRepository:
    """Tests for SQLite VersionRepository."""

    @pytest.fixture(autouse=True)
    def setup_repo(self):
        """Set up test fixtures."""
        from caf.database.db import init_db

        init_db()
        self.repo = SQLiteVersionRepository()
        for item in self.repo.get_all():
            self.repo.delete(item.id)
        # Also clear instructions to avoid FK conflicts
        from caf.repositories.sqlite_instruction_repository import (
            SQLiteInstructionRepository,
        )

        inst_repo = SQLiteInstructionRepository()
        for item in inst_repo.get_all():
            inst_repo.delete(item.id)

    def teardown_method(self):
        """Clean up after tests."""
        for item in self.repo.get_all():
            self.repo.delete(item.id)
        from caf.repositories.sqlite_instruction_repository import (
            SQLiteInstructionRepository,
        )

        inst_repo = SQLiteInstructionRepository()
        for item in inst_repo.get_all():
            inst_repo.delete(item.id)

    def _create_instruction(self, instruction_id="sqlite-inst-1"):
        """Helper to create an instruction for FK."""
        inst_repo = SQLiteInstructionRepository()
        inst = Instruction(
            id=instruction_id,
            template_name="Test",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        inst_repo.save(inst)

    def test_save(self):
        """Test saving a version."""
        self._create_instruction("sqlite-inst-1")
        version = Version(
            id="sqlite-ver-1",
            instruction_id="sqlite-inst-1",
            version_number=1,
            change_summary="SQLite version",
            created_by="test-user",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(version)

        retrieved = self.repo.get_by_id(version.id)
        assert retrieved.id == version.id
        assert retrieved.change_summary == "SQLite version"

    def test_get_by_id(self):
        """Test retrieving a version by ID."""
        self._create_instruction("sqlite-inst-1")
        version = Version(
            id="sqlite-test-1",
            instruction_id="sqlite-inst-1",
            version_number=1,
            change_summary="Test",
            created_by="test-user",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(version)

        retrieved = self.repo.get_by_id("sqlite-test-1")
        assert retrieved.id == "sqlite-test-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all versions."""
        self._create_instruction("inst-0")
        self._create_instruction("inst-1")
        self._create_instruction("inst-2")
        for i in range(3):
            v = Version(
                id=f"sqlite-ver-{i}",
                instruction_id=f"inst-{i}",
                version_number=1,
                change_summary=f"Change {i}",
                created_by="test",
                parent_version_id=None,
                created_at=datetime.now(UTC),
            )
            self.repo.save(v)

        assert len([i for i in self.repo.get_all() if i.id.startswith("sqlite-")]) == 3

    def test_delete(self):
        """Test deleting a version."""
        self._create_instruction("inst-1")
        version = Version(
            id="sqlite-delete",
            instruction_id="inst-1",
            version_number=1,
            change_summary="Test",
            created_by="test",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(version)

        assert self.repo.get_by_id(version.id) is not None
        self.repo.delete(version.id)

        with pytest.raises(ValueError):
            self.repo.get_by_id(version.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing version."""
        self._create_instruction("inst-1")
        version = Version(
            id="sqlite-overwrite",
            instruction_id="inst-1",
            version_number=1,
            change_summary="Original",
            created_by="test",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(version)

        updated = Version(
            id=version.id,
            instruction_id=version.instruction_id,
            version_number=version.version_number,
            change_summary="Updated",
            created_by="test",
            parent_version_id=version.parent_version_id,
            created_at=version.created_at,
        )
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(version.id)
        assert retrieved.change_summary == "Updated"

    def test_get_by_instruction_id(self):
        """Test retrieving versions by instruction ID."""
        self._create_instruction("sqlite-inst-1")
        for i in range(3):
            v = Version(
                id=f"sqlite-v-{i}",
                instruction_id="sqlite-inst-1",
                version_number=i + 1,
                change_summary=f"Change {i}",
                created_by="test",
                parent_version_id=None,
                created_at=datetime.now(UTC),
            )
            self.repo.save(v)

        versions = self.repo.get_by_instruction_id("sqlite-inst-1")
        assert len(versions) == 3
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2
        assert versions[2].version_number == 3

    def test_version_ordering(self):
        """Test versions are ordered by version_number."""
        self._create_instruction("sqlite-order-inst")

        v2 = Version(
            id="v2",
            instruction_id="sqlite-order-inst",
            version_number=2,
            change_summary="C2",
            created_by="t",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        v1 = Version(
            id="v1",
            instruction_id="sqlite-order-inst",
            version_number=1,
            change_summary="C1",
            created_by="t",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        v3 = Version(
            id="v3",
            instruction_id="sqlite-order-inst",
            version_number=3,
            change_summary="C3",
            created_by="t",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )

        self.repo.save(v2)
        self.repo.save(v1)
        self.repo.save(v3)

        versions = self.repo.get_by_instruction_id("sqlite-order-inst")
        assert len(versions) == 3
        assert versions[0].version_number == 1
        assert versions[1].version_number == 2
        assert versions[2].version_number == 3

    def test_parent_version_id_preserved(self):
        """Test parent_version_id is preserved."""
        self._create_instruction("sqlite-inst")
        # First create the parent version
        parent = Version(
            id="sqlite-parent-1",
            instruction_id="sqlite-inst",
            version_number=1,
            change_summary="Parent",
            created_by="test",
            parent_version_id=None,
            created_at=datetime.now(UTC),
        )
        self.repo.save(parent)

        parent_id = "sqlite-parent-1"
        child = Version(
            id="sqlite-child",
            instruction_id="sqlite-inst",
            version_number=2,  # Different version number
            change_summary="Child",
            created_by="test",
            parent_version_id=parent_id,
            created_at=datetime.now(UTC),
        )
        self.repo.save(child)

        retrieved = self.repo.get_by_id(child.id)
        assert retrieved.parent_version_id == parent_id

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        self._create_instruction("inst")

        items = [
            Version(
                id=f"order-{i}",
                instruction_id="inst",
                version_number=i,
                change_summary="C",
                created_by="t",
                parent_version_id=None,
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
