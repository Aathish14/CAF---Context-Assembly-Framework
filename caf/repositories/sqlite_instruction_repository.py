"""SQLite-backed Instruction repository for CAF application."""

import json

from caf.models.instruction import Instruction
from caf.repositories.sqlite_base_repository import SQLiteBaseRepository


class SQLiteInstructionRepository(SQLiteBaseRepository[Instruction]):
    """SQLite-backed repository for Instruction objects."""

    @property
    def table_name(self) -> str:
        return "instructions"

    @property
    def id_column(self) -> str:
        return "id"

    @property
    def order_by_column(self) -> str:
        return "created_at"

    def _get_columns(self) -> list[str]:
        return [
            "id",
            "template_name",
            "context",
            "assembled_instruction",
            "created_at",
            "version",
        ]

    def _model_to_row(self, instruction: Instruction) -> tuple:
        """Convert Instruction to database row tuple."""
        return (
            instruction.id,
            instruction.template_name,
            json.dumps(instruction.context),
            instruction.assembled_instruction,
            self._to_db_datetime(instruction.created_at),
            instruction.version,
        )

    def _row_to_model(self, row: dict) -> Instruction:
        """Convert a database row to an Instruction object."""
        return Instruction(
            id=row["id"],
            template_name=row["template_name"],
            context=json.loads(row["context"]) if row["context"] else {},
            assembled_instruction=row["assembled_instruction"],
            created_at=self._from_db_datetime(row["created_at"]),
            version=row["version"],
        )


# Global SQLite instruction repository instance
sqlite_instruction_repository = SQLiteInstructionRepository()
