"""Unit tests for ContextBuilder."""

import pytest

from caf.models.context import Context
from caf.services.context_builder import ContextBuilder


class TestContextBuilder:
    """Tests for ContextBuilder class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.builder = ContextBuilder()
        self.valid_answers = {
            "objective": "Write a blog post",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["< 1000 words", "Include code examples"],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }

    def test_successful_context_creation(self):
        """Test successful Context creation with all fields."""
        context = self.builder.build(self.valid_answers)

        assert isinstance(context, Context)
        assert context.objective == "Write a blog post"
        assert context.audience == "Developers"
        assert context.tone == "Technical"
        assert context.constraints == ["< 1000 words", "Include code examples"]
        assert context.output_format == "Markdown"
        assert context.risk_level == "Low"
        assert context.language == "English"
        assert context.word_limit == 1000
        assert context.purpose == "Education"
        assert context.business_type == "SaaS"

    def test_empty_constraints_list(self):
        """Test Context creation with empty constraints list."""
        answers = {**self.valid_answers, "constraints": []}
        context = self.builder.build(answers)

        assert context.constraints == []

    def test_optional_word_limit_none(self):
        """Test Context creation with optional word_limit as None."""
        answers = {**self.valid_answers, "word_limit": None}
        context = self.builder.build(answers)

        assert context.word_limit is None

    def test_optional_word_limit_omitted(self):
        """Test Context creation with word_limit omitted (uses default)."""
        answers = {k: v for k, v in self.valid_answers.items() if k != "word_limit"}
        context = self.builder.build(answers)

        assert context.word_limit is None

    def test_invalid_input_missing_required_field(self):
        """Test Context creation fails with missing required field."""
        answers = {k: v for k, v in self.valid_answers.items() if k != "objective"}

        with pytest.raises(ValueError):
            self.builder.build(answers)

    def test_invalid_input_missing_multiple_required_fields(self):
        """Test Context creation fails with multiple missing required fields."""
        answers = {"objective": "Test"}

        with pytest.raises(ValueError):
            self.builder.build(answers)

    def test_invalid_input_wrong_type(self):
        """Test Context creation fails with wrong type for word_limit."""
        answers = {**self.valid_answers, "word_limit": "not an int"}

        with pytest.raises(ValueError):
            self.builder.build(answers)

    def test_deterministic_context_creation(self):
        """Test that Context creation is deterministic."""
        context1 = self.builder.build(self.valid_answers)
        context2 = self.builder.build(self.valid_answers)

        assert context1 == context2
        assert context1.model_dump() == context2.model_dump()

    def test_correct_field_mapping(self):
        """Test that all fields are correctly mapped from answers to Context."""
        context = self.builder.build(self.valid_answers)
        dumped = context.model_dump()

        for key, value in self.valid_answers.items():
            assert dumped[key] == value, f"Field '{key}' not correctly mapped"

    def test_preserves_user_input_exactly(self):
        """Test that user input is preserved exactly without modification."""
        answers = {
            "objective": "  Leading/trailing spaces  ",
            "audience": "Developers",
            "tone": "Technical",
            "constraints": ["  constraint with spaces  "],
            "output_format": "Markdown",
            "risk_level": "Low",
            "language": "English",
            "word_limit": 1000,
            "purpose": "Education",
            "business_type": "SaaS",
        }
        context = self.builder.build(answers)

        assert context.objective == "  Leading/trailing spaces  "
        assert context.constraints == ["  constraint with spaces  "]

    def test_context_immutability_after_creation(self):
        """Test that Context object can be used after creation."""
        context = self.builder.build(self.valid_answers)

        assert context.model_dump() == self.valid_answers
        json_output = context.model_dump_json()
        assert "Write a blog post" in json_output
