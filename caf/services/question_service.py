"""
Question service for loading and managing questions.
"""

import json
from pathlib import Path
from typing import Any

from caf.services.validation_service import ValidationService


class QuestionService:
    """Service for managing questions."""

    def __init__(self, validation_service: ValidationService | None = None):
        self._questions: list[dict[str, Any]] = []
        self._validation_service = validation_service or ValidationService()
        self._load_questions()

    def _load_questions(self) -> None:
        """Load questions from JSON configuration file."""
        # Look for questions.json in the config directory
        config_dir = Path(__file__).parent.parent / "config"
        questions_file = config_dir / "questions.json"

        try:
            with open(questions_file, encoding="utf-8") as f:
                data = json.load(f)
                self._questions = data.get("questions", [])
        except FileNotFoundError:
            # Create default questions if file doesn't exist
            self._questions = self._get_default_questions()
            self._save_questions(questions_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in questions file: {e}") from e

    def _save_questions(self, path: Path) -> None:
        """Save questions to JSON file.

        Args:
            path: Path to questions JSON file
        """
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {"questions": self._questions}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _get_default_questions(self) -> list[dict[str, Any]]:
        """Get default questions for demonstration.

        Returns:
            List of default question dictionaries
        """
        return [
            {
                "id": "name",
                "text": "What is your name?",
                "type": "text",
                "required": True,
                "placeholder": "Enter your full name",
            },
            {
                "id": "email",
                "text": "What is your email address?",
                "type": "text",
                "required": True,
                "placeholder": "Enter your email address",
            },
            {
                "id": "age_group",
                "text": "Which age group do you belong to?",
                "type": "select",
                "required": True,
                "options": [
                    "Under 18",
                    "18-24",
                    "25-34",
                    "35-44",
                    "45-54",
                    "55-64",
                    "65 or over",
                ],
            },
            {
                "id": "occupation",
                "text": "What is your current occupation?",
                "type": "select",
                "required": True,
                "options": [
                    "Student",
                    "Software Engineer",
                    "Designer",
                    "Product Manager",
                    "Data Scientist",
                    "Teacher",
                    "Healthcare Professional",
                    "Other",
                ],
            },
            {
                "id": "tech_stack",
                "text": "Which technologies do you work with? (Select all that apply)",
                "type": "multiselect",
                "required": False,
                "options": [
                    "Python",
                    "JavaScript",
                    "Java",
                    "C#",
                    "Go",
                    "Rust",
                    "SQL",
                    "NoSQL",
                    "Docker",
                    "Kubernetes",
                    "AWS",
                    "Azure",
                    "GCP",
                ],
            },
            {
                "id": "experience",
                "text": "How would you rate your overall experience with similar frameworks?",
                "type": "select",
                "required": True,
                "options": ["Excellent", "Good", "Average", "Poor", "Very Poor"],
            },
            {
                "id": "feedback",
                "text": "Any additional comments or feedback?",
                "type": "text",
                "required": False,
                "placeholder": "Please share your thoughts...",
            },
        ]

    def get_all_questions(self) -> list[dict[str, Any]]:
        """Get all questions.

        Returns:
            List of question dictionaries
        """
        return self._questions.copy()

    def get_question_by_id(self, question_id: str) -> dict[str, Any] | None:
        """Get a question by its ID.

        Args:
            question_id: The ID of the question to retrieve

        Returns:
            Question dictionary if found, None otherwise
        """
        for question in self._questions:
            if question["id"] == question_id:
                return question.copy()
        return None

    def validate_answer(self, question: dict[str, Any], answer: Any) -> bool:
        """Validate an answer for a given question.

        Delegates to ValidationService for single validation authority.

        Args:
            question: Question dictionary
            answer: User's answer to validate

        Returns:
            True if answer is valid, False otherwise
        """
        result = self._validation_service.validate_answer(question, answer)
        return result.is_valid


# Global question service instance for backward compatibility
question_service = QuestionService()
