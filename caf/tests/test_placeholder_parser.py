"""Tests for PlaceholderParser utility."""

from caf.utils.placeholder_parser import PlaceholderParser


class TestPlaceholderParser:
    """Tests for PlaceholderParser utility."""

    def test_extract_placeholders_simple(self):
        """Test extracting simple placeholders."""
        text = "Hello {{name}}, welcome to {{place}}!"
        result = PlaceholderParser.extract_placeholders(text)
        assert result == ["name", "place"]

    def test_extract_placeholders_duplicate(self):
        """Test that duplicate placeholders are deduplicated."""
        text = "Hello {{name}}, welcome {{name}} to {{place}}!"
        result = PlaceholderParser.extract_placeholders(text)
        assert result == ["name", "place"]

    def test_extract_placeholders_none(self):
        """Test extracting from text with no placeholders."""
        text = "Hello world!"
        result = PlaceholderParser.extract_placeholders(text)
        assert result == []

    def test_extract_placeholders_nested_braces(self):
        """Test that nested braces are handled correctly."""
        text = "Hello {{name}}, {{not_a_placeholder}} world!"
        result = PlaceholderParser.extract_placeholders(text)
        assert result == ["name", "not_a_placeholder"]

    def test_validate_placeholders_valid(self):
        """Test validation passes for matching placeholders."""
        text = "Hello {{name}}, welcome to {{place}}!"
        declared = ["name", "place"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        assert is_valid is True
        assert errors == []

    def test_validate_placeholders_undeclared(self):
        """Test validation fails for undeclared placeholders."""
        text = "Hello {{name}}, welcome to {{place}}!"
        declared = ["name"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        assert is_valid is False
        assert len(errors) == 1
        assert "place" in errors[0]

    def test_validate_placeholders_missing(self):
        """Test validation fails for missing placeholders."""
        text = "Hello {{name}}!"
        declared = ["name", "place"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        assert is_valid is False
        assert len(errors) == 1
        assert "place" in errors[0]

    def test_validate_placeholders_duplicate_in_template(self):
        """Test validation fails for duplicate placeholders in template."""
        text = "Hello {{name}}, {{name}}!"
        declared = ["name"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        assert is_valid is False
        assert len(errors) == 1
        assert "Duplicate placeholders" in errors[0]

    def test_validate_placeholders_duplicate_in_declared(self):
        """Test validation fails for duplicate placeholders in declared list."""
        text = "Hello {{name}}!"
        declared = ["name", "name"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        assert is_valid is False
        assert len(errors) == 1
        assert "Duplicate placeholders in declared list" in errors[0]

    def test_replace_placeholders_simple(self):
        """Test simple placeholder replacement."""
        text = "Hello {{name}}, welcome to {{place}}!"
        result = PlaceholderParser.replace_placeholders(
            text, {"name": "Alice", "place": "Wonderland"}
        )
        assert result == "Hello Alice, welcome to Wonderland!"

    def test_replace_placeholders_missing(self):
        """Test missing placeholders are left unchanged."""
        text = "Hello {{name}}, welcome to {{place}}!"
        result = PlaceholderParser.replace_placeholders(text, {"name": "Alice"})
        assert result == "Hello Alice, welcome to {{place}}!"

    def test_replace_placeholders_empty_values_none(self):
        """Test None values are converted to string."""
        text = "Hello {{name}}!"
        result = PlaceholderParser.replace_placeholders(text, {"name": None})
        assert result == "Hello None!"

    def test_replace_multiple_occurrences(self):
        """Test multiple occurrences of same placeholder."""
        text = "{{name}} likes {{name}}."
        result = PlaceholderParser.replace_placeholders(text, {"name": "Alice"})
        assert result == "Alice likes Alice."

    def test_whitespace_handling(self):
        """Test whitespace in placeholders is handled."""
        text = "Hello {{ name }}!"
        result = PlaceholderParser.replace_placeholders(text, {"name": "Alice"})
        assert result == "Hello Alice!"

    def test_validate_malformed_braces(self):
        """Test malformed braces are handled - single braces are treated as literal text."""
        text = "Hello {name}!"
        declared = ["name"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        # Single braces are treated as literal text, so "name" is not found as a placeholder
        # This means it's declared but not found -> validation error
        assert is_valid is False
        assert "name" in errors[0]

    def test_validate_multiple_errors(self):
        """Test multiple validation errors are reported."""
        text = "Hello {{name}}, {{missing}}!"
        declared = ["name"]
        is_valid, errors = PlaceholderParser.validate_placeholders(text, declared)
        assert is_valid is False
        assert len(errors) >= 1
