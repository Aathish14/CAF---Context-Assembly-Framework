"""Template service for CAF application."""

import json
from pathlib import Path

from caf.models.template import Template


class TemplateService:
    """Service for loading and managing templates."""

    DEFAULT_TEMPLATES_PATH = Path("caf/config/templates/default_templates.json")

    def __init__(self, templates_path: Path | None = None):
        """Initialize TemplateService.

        Args:
            templates_path: Optional path to templates JSON file.
        """
        self._templates_path = templates_path or self.DEFAULT_TEMPLATES_PATH
        self._templates: list[Template] = []
        self._load_templates()

    def _load_templates(self) -> None:
        """Load and validate templates from JSON file.

        Raises:
            FileNotFoundError: If templates file does not exist.
            json.JSONDecodeError: If JSON is invalid.
            ValueError: If template validation fails.
        """
        with open(self._templates_path, encoding="utf-8") as f:
            data = json.load(f)
        self._templates = [Template(**item) for item in data]

    def get_all(self) -> list[Template]:
        """Get all loaded templates.

        Returns:
            List of all Template objects.
        """
        return self._templates

    def get_by_id(self, template_id: str) -> Template:
        """Get template by ID.

        Args:
            template_id: ID of the template to retrieve.

        Returns:
            Template object.

        Raises:
            ValueError: If template with given ID does not exist.
        """
        for template in self._templates:
            if template.id == template_id:
                return template
        raise ValueError(f"Template with id '{template_id}' not found")

    def get_by_category(self, category: str) -> list[Template]:
        """Get templates by category.

        Args:
            category: Category to filter by.

        Returns:
            List of Template objects in the given category.
        """
        return [t for t in self._templates if t.category == category]


# Global template service instance for backward compatibility
template_service = TemplateService()
