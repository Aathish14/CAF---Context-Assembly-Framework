"""Tests for InstructionRepository (in-memory and SQLite)."""

import uuid
from datetime import UTC, datetime

import pytest

from caf.models.instruction import Instruction
from caf.repositories.sqlite_instruction_repository import SQLiteInstructionRepository

# ============================================================================
# Parameterized Tests for Both Repository Types
# ============================================================================


class TestInstructionRepositoryBase:
    """Base test class for InstructionRepository (both in-memory and SQLite)."""

    @pytest.fixture(autouse=True)
    def setup_repo(self, instruction_repo):
        """Set up repository for each test."""
        self.repo = instruction_repo
        # Clear any existing data
        for item in self.repo.get_all():
            self.repo.delete(item.id)

    def make_instruction(self, **kwargs):
        """Create a test instruction."""
        {
            "id": str(uuid.uuid4()),
            "template_name": "Test Template",
            "context": {"objective": "test"},
            "assembled_instruction": "Test instruction",
            "created_at": datetime.now(UTC),
            "version": 1,
        }
        return Instruction(
            **{
                **{
                    "id": str(uuid.uuid4()),
                    "template_name": "Test Template",
                    "context": {"objective": "test"},
                    "assembled_instruction": "Test instruction",
                    "created_at": datetime.now(UTC),
                    "version": 1,
                },
                **kwargs,
            }
        )

    def test_save(self):
        """Test saving an instruction."""
        instruction = Instruction(
            id="test-id",
            template_name="Test Template",
            context={"objective": "test"},
            assembled_instruction="Test instruction",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        retrieved = self.repo.get_by_id(instruction.id)
        assert retrieved.id == instruction.id
        assert retrieved.template_name == "Test Template"
        assert retrieved.context == {"objective": "test"}
        assert retrieved.assembled_instruction == "Test instruction"
        assert retrieved.version == 1

    def test_get_by_id(self):
        """Test retrieving an instruction by ID."""
        instruction = Instruction(
            id="test-id-1",
            template_name="Test Template",
            context={"objective": "test"},
            assembled_instruction="Test instruction",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        retrieved = self.repo.get_by_id("test-id-1")
        assert retrieved.id == "test-id-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all instructions."""
        for i in range(3):
            inst = Instruction(
                id=f"inst-{i}",
                template_name=f"Template {i}",
                context={},
                assembled_instruction=f"Test {i}",
                created_at=datetime.now(UTC),
                version=1,
            )
            self.repo.save(inst)

        self.repo.get_all()
        assert len([i for i in self.repo.get_all() if i.id.startswith("inst-")]) == 3

    def test_delete(self):
        """Test deleting an instruction."""
        instruction = Instruction(
            id="test-delete",
            template_name="Test",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        # Verify it exists
        assert self.repo.get_by_id(instruction.id) is not None

        # Delete
        self.repo.delete(instruction.id)

        # Verify it's gone
        with pytest.raises(ValueError):
            self.repo.get_by_id(instruction.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing item."""
        instruction = Instruction(
            id="overwrite-test",
            template_name="Original",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        # Update with new template name
        updated = Instruction(
            id=instruction.id,
            template_name="Updated",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(instruction.id)
        assert retrieved.template_name == "Updated"

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        # Clear repo
        for item in self.repo.get_all():
            self.repo.delete(item.id)

        items = [
            Instruction(
                id="inst-1",
                template_name="First",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
            ),
            Instruction(
                id="inst-2",
                template_name="Second",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
            ),
            Instruction(
                id="inst-3",
                template_name="Third",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
            ),
        ]

        for item in items:
            self.repo.save(item)

        self.repo.get_all()
        saved = [i for i in self.repo.get_all() if i.id.startswith("inst-")]

        assert len(saved) == 3
        assert saved[0].id == "inst-1"
        assert saved[1].id == "inst-2"
        assert saved[2].id == "inst-3"


# ============================================================================
# Parameterized Tests for Both Repository Types
# ============================================================================


class TestInstructionRepository:
    """Tests for in-memory InstructionRepository."""

    @pytest.fixture(autouse=True)
    def setup_repo(self, mem_instruction_repo):
        self.repo = mem_instruction_repo
        # Clear any existing data
        for item in self.repo.get_all():
            self.repo.delete(item.id)

    def make_instruction(self, **kwargs):
        from caf.models.instruction import Instruction

        {
            "id": str(uuid.uuid4()),
            "template_name": "Test Template",
            "context": {"objective": "test"},
            "assembled_instruction": "Test instruction",
            "created_at": datetime.now(UTC),
            "version": 1,
        }
        return Instruction(
            **{
                **{
                    "id": str(uuid.uuid4()),
                    "template_name": "Test Template",
                    "context": {"objective": "test"},
                    "assembled_instruction": "Test instruction",
                    "created_at": datetime.now(UTC),
                    "version": 1,
                },
                **kwargs,
            }
        )

    def test_save(self):
        """Test saving an instruction."""
        instruction = Instruction(
            id="test-id",
            template_name="Test Template",
            context={"objective": "test"},
            assembled_instruction="Test instruction",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        retrieved = self.repo.get_by_id(instruction.id)
        assert retrieved.id == instruction.id
        assert retrieved.template_name == "Test Template"
        assert retrieved.context == {"objective": "test"}
        assert retrieved.assembled_instruction == "Test instruction"
        assert retrieved.version == 1

    def test_get_by_id(self):
        """Test retrieving an instruction by ID."""
        instruction = Instruction(
            id="test-id-1",
            template_name="Test Template",
            context={"objective": "test"},
            assembled_instruction="Test instruction",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        retrieved = self.repo.get_by_id("test-id-1")
        assert retrieved.id == "test-id-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all instructions."""
        for i in range(3):
            inst = Instruction(
                id=f"inst-{i}",
                template_name=f"Template {i}",
                context={},
                assembled_instruction=f"Test {i}",
                created_at=datetime.now(UTC),
                version=1,
            )
            self.repo.save(inst)

        self.repo.get_all()
        assert len([i for i in self.repo.get_all() if i.id.startswith("inst-")]) == 3

    def test_delete(self):
        """Test deleting an instruction."""
        instruction = Instruction(
            id="test-delete",
            template_name="Test",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        # Verify it exists
        assert self.repo.get_by_id(instruction.id) is not None

        # Delete
        self.repo.delete(instruction.id)

        # Verify it's gone
        with pytest.raises(ValueError):
            self.repo.get_by_id(instruction.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing item."""
        """TestInstructionRepository."""
        from caf.models.instruction import Instruction

        instruction = Instruction(
            id="overwrite-test",
            template_name="Original",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        # Update with new template name
        updated = Instruction(
            id=instruction.id,
            template_name="Updated",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(instruction.id)
        assert retrieved.template_name == "Updated"

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        # Clear repo
        for item in self.repo.get_all():
            self.repo.delete(item.id)

        items = [
            Instruction(
                id="inst-1",
                template_name="First",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
            ),
            Instruction(
                id="inst-2",
                template_name="Second",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
            ),
            Instruction(
                id="inst-3",
                template_name="Third",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
            ),
        ]

        for item in items:
            self.repo.save(item)

        self.repo.get_all()
        saved = [i for i in self.repo.get_all() if i.id.startswith("inst-")]

        assert len(saved) == 3
        assert saved[0].id == "inst-1"
        assert saved[1].id == "inst-2"
        assert saved[2].id == "inst-3"


class TestSQLiteInstructionRepository:
    """Tests for SQLite InstructionRepository."""

    def setup_method(self):
        """Set up test fixtures."""
        from caf.database.db import init_db

        init_db()
        self.repo = SQLiteInstructionRepository()
        # Clear any existing data
        for item in self.repo.get_all():
            self.repo.delete(item.id)

    def teardown_method(self):
        """Clean up after tests."""
        for item in self.repo.get_all():
            self.repo.delete(item.id)

    def test_save(self):
        """Test saving an instruction."""
        from caf.models.instruction import Instruction

        instruction = Instruction(
            id="test-sqlite-1",
            template_name="SQLite Template",
            context={"objective": "test"},
            assembled_instruction="Test instruction",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        retrieved = self.repo.get_by_id(instruction.id)
        assert retrieved.id == instruction.id
        assert retrieved.template_name == "SQLite Template"

    def test_get_by_id(self):
        """Test retrieving an instruction by ID."""
        from caf.models.instruction import Instruction

        instruction = Instruction(
            id="sqlite-test-1",
            template_name="SQLite Template",
            context={"objective": "test"},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        retrieved = self.repo.get_by_id("sqlite-test-1")
        assert retrieved.id == "sqlite-test-1"

        # Not found
        with pytest.raises(ValueError):
            self.repo.get_by_id("non-existent")

    def test_get_all(self):
        """Test retrieving all instructions."""
        from caf.models.instruction import Instruction

        for i in range(3):
            inst = Instruction(
                id=f"sqlite-inst-{i}",
                template_name=f"Template {i}",
                context={},
                assembled_instruction=f"Test {i}",
                created_at=datetime.now(UTC),
                version=1,
            )
            self.repo.save(inst)

        assert len([i for i in self.repo.get_all() if i.id.startswith("sqlite-")]) == 3

    def test_delete(self):
        """Test deleting an instruction."""
        from caf.models.instruction import Instruction

        instruction = Instruction(
            id="sqlite-delete",
            template_name="Test",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        # Verify it exists
        assert self.repo.get_by_id(instruction.id) is not None

        # Delete
        self.repo.delete(instruction.id)

        # Verify it's gone
        with pytest.raises(ValueError):
            self.repo.get_by_id(instruction.id)

    def test_overwrite_existing(self):
        """Test overwriting an existing item."""
        from caf.models.instruction import Instruction

        instruction = Instruction(
            id="sqlite-overwrite",
            template_name="Original",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(instruction)

        # Update with new template name
        updated = Instruction(
            id=instruction.id,
            template_name="Updated",
            context={},
            assembled_instruction="Test",
            created_at=datetime.now(UTC),
            version=1,
        )
        self.repo.save(updated)

        retrieved = self.repo.get_by_id(instruction.id)
        assert retrieved.template_name == "Updated"

    def test_insertion_order_preserved(self):
        """Test that insertion order is preserved in get_all()."""
        from caf.models.instruction import Instruction

        for item in self.repo.get_all():
            self.repo.delete(item.id)

        items = [
            Instruction(
                id=f"order-{i}",
                template_name=f"Template {i}",
                context={},
                assembled_instruction="Test",
                created_at=datetime.now(UTC),
                version=1,
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
