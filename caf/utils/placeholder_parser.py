"""Placeholder parser utility for CAF templates."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParseResult:
    """Result of placeholder parsing."""

    placeholders: list[str]
    errors: list[str]


class PlaceholderParser:
    """Utility for parsing and validating template placeholders."""

    PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    @classmethod
    def extract_placeholders(cls, template_text: str) -> list[str]:
        """Extract all placeholder names from template text.

        Args:
            template_text: Template text with {{placeholder}} patterns.

        Returns:
            List of unique placeholder names found in the template.
        """
        matches = cls.PLACEHOLDER_PATTERN.findall(template_text)
        # Return unique placeholders preserving order of first appearance
        seen = set()
        result = []
        for m in matches:
            if m not in seen:
                seen.add(m)
                result.append(m)
        return result

    @classmethod
    def extract_placeholders_with_duplicates(cls, template_text: str) -> list[str]:
        """Extract all placeholder names from template text, including duplicates.

        Args:
            template_text: Template text with {{placeholder}} patterns.

        Returns:
            List of placeholder names found in the template, including duplicates.
        """
        matches = cls.PLACEHOLDER_PATTERN.findall(template_text)
        return matches

    @classmethod
    def validate_placeholders(
        cls, template_text: str, declared_placeholders: list[str]
    ) -> tuple[bool, list[str]]:
        """Validate that template placeholders match declared placeholders.

        Args:
            template_text: Template text with {{placeholder}} patterns.
            declared_placeholders: List of placeholder names declared in template.

        Returns:
            Tuple of (is_valid, list_of_errors).
        """
        errors = []
        found = cls.extract_placeholders(template_text)
        found_with_duplicates = cls.extract_placeholders_with_duplicates(template_text)
        declared_set = set(declared_placeholders)
        found_set = set(found)

        # Check for placeholders in template but not declared
        undeclared = found_set - declared_set
        if undeclared:
            errors.append(
                f"Placeholders found in template_text but not declared in placeholders: {sorted(undeclared)}"
            )

        # Check for declared placeholders not used in template_text
        missing = declared_set - found_set
        if missing:
            errors.append(
                f"Placeholders declared in placeholders but not found in template_text: {sorted(missing)}"
            )

        # Check for duplicate placeholders in template_text
        if len(found) != len(set(found)):
            duplicates = [p for p in found if found.count(p) > 1]
            errors.append(
                f"Duplicate placeholders in template_text: {sorted(set(duplicates))}"
            )
        else:
            # Check for duplicates using the version with duplicates
            if len(
                found_with_duplicates := cls.extract_placeholders_with_duplicates(
                    template_text
                )
            ) != len(set(found_with_duplicates)):
                duplicates = [
                    p
                    for p in found_with_duplicates
                    if found_with_duplicates.count(p) > 1
                ]
                errors.append(
                    f"Duplicate placeholders in template_text: {sorted(set(duplicates))}"
                )

        # Check for duplicate placeholders in declared list
        if len(declared_placeholders) != len(set(declared_placeholders)):
            duplicates = [
                p for p in declared_placeholders if declared_placeholders.count(p) > 1
            ]
            errors.append(
                f"Duplicate placeholders in declared list: {sorted(set(duplicates))}"
            )

        return len(errors) == 0, errors

    @classmethod
    def replace_placeholders(cls, template_text: str, values: dict) -> str:
        """Replace placeholders in template text with values from context.

        Args:
            template_text: Template text with {{placeholder}} patterns.
            values: Dictionary of context values.

        Returns:
            Template text with placeholders replaced. Missing placeholders
            are left unchanged.
        """

        def replace_match(match: re.Match[str]) -> str:
            key = match.group(1)
            return str(values.get(key, match.group(0)))

        return cls.PLACEHOLDER_PATTERN.sub(replace_match, template_text)
