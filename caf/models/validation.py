"""
Validation models for structured validation results.
"""

from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """Structured result of a validation check."""

    is_valid: bool
    question_id: str
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def add_error(self, error: str) -> None:
        """Add an error and mark as invalid."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add a warning without affecting validity."""
        self.warnings.append(warning)

    @classmethod
    def valid(cls, question_id: str) -> "ValidationResult":
        """Create a valid result."""
        return cls(is_valid=True, question_id=question_id)

    @classmethod
    def invalid(cls, question_id: str, errors: list[str]) -> "ValidationResult":
        """Create an invalid result with errors."""
        return cls(is_valid=False, question_id=question_id, errors=errors)
