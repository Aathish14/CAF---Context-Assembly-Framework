"""
Validation service for validating user answers against question definitions.
"""

from typing import Any

from caf.models.validation import ValidationResult


class ValidationService:
    """Service for validating answers against question schemas."""

    SUPPORTED_TYPES = {"text", "select", "multiselect"}

    def validate_answer(
        self, question: dict[str, Any], answer: Any
    ) -> ValidationResult:
        """Validate a single answer against its question definition.

        Args:
            question: Question dictionary with id, type, required, options, min_length, max_length
            answer: User's answer to validate

        Returns:
            ValidationResult with validation outcome
        """
        question_id = question.get("id", "unknown")
        result = ValidationResult.valid(question_id)

        # Check for unsupported question type
        question_type = question.get("type")
        if question_type not in self.SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported question type: '{question_type}' for question '{question_id}'. "
                f"Supported types: {self.SUPPORTED_TYPES}"
            )

        # Required field validation
        if question.get("required", False):
            if not self._is_required_valid(question_type, answer):
                result.add_error(f"Question '{question_id}' is required")
                return result

        # Type-specific validation (only if answer is provided)
        if answer is not None and answer != "":
            if question_type == "text":
                self._validate_text(question, answer, result)
            elif question_type == "select":
                self._validate_select(question, answer, result)
            elif question_type == "multiselect":
                self._validate_multiselect(question, answer, result)

        return result

    def validate_all(
        self, questions: list[dict[str, Any]], answers: dict[str, Any]
    ) -> dict[str, ValidationResult]:
        """Validate all answers against their question definitions.

        Args:
            questions: List of question dictionaries
            answers: Dict mapping question_id to user answer

        Returns:
            Dict mapping question_id to ValidationResult
        """
        results = {}
        for question in questions:
            question_id = question.get("id", "unknown")
            answer = answers.get(question_id)
            results[question_id] = self.validate_answer(question, answer)
        return results

    def _is_required_valid(self, question_type: str, answer: Any) -> bool:
        """Check if a required field has a valid value."""
        if question_type == "text":
            return isinstance(answer, str) and len(answer.strip()) > 0
        elif question_type == "select":
            return answer is not None and answer != ""
        elif question_type == "multiselect":
            return isinstance(answer, list) and len(answer) > 0
        return False

    def _validate_text(
        self, question: dict[str, Any], answer: Any, result: ValidationResult
    ) -> None:
        """Validate text input with min/max length constraints."""
        if not isinstance(answer, str):
            result.add_error("Answer must be a string")
            return

        min_length = question.get("min_length")
        max_length = question.get("max_length")

        if min_length is not None and len(answer) < min_length:
            result.add_error(f"Minimum length is {min_length} characters")

        if max_length is not None and len(answer) > max_length:
            result.add_error(f"Maximum length is {max_length} characters")

    def _validate_select(
        self, question: dict[str, Any], answer: Any, result: ValidationResult
    ) -> None:
        """Validate select input against allowed options."""
        options = question.get("options", [])
        if not options:
            result.add_warning("No options defined for select question")
            return

        if answer not in options:
            result.add_error(f"Value '{answer}' is not in allowed options")

    def _validate_multiselect(
        self, question: dict[str, Any], answer: Any, result: ValidationResult
    ) -> None:
        """Validate multiselect input against allowed options."""
        options = question.get("options", [])
        if not options:
            result.add_warning("No options defined for multiselect question")
            return

        if not isinstance(answer, list):
            result.add_error("Answer must be a list")
            return

        invalid_values = [v for v in answer if v not in options]
        if invalid_values:
            result.add_error(f"Values {invalid_values} are not in allowed options")


# Global validation service instance
validation_service = ValidationService()
