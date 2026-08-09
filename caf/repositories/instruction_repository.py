"""Instruction repository for CAF application."""

from caf.models.instruction import Instruction
from caf.repositories.base_repository import BaseRepository


class InstructionRepository(BaseRepository[Instruction]):
    """In-memory repository for Instruction objects."""


# Global instruction repository instance
instruction_repository = InstructionRepository()
