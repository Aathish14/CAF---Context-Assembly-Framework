"""Template model for CAF application."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field, model_validator

from caf.utils.placeholder_parser import PlaceholderParser


class Template(BaseModel):
    """Template model representing an instruction template."""

    id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    description: str = Field(..., description="Description of the template")
    template_text: str = Field(..., description="The template text with placeholders")
    placeholders: list[str] = Field(
        ..., description="List of placeholder names in the template"
    )
    category: str = Field(..., description="Category of the template")
    version: int = Field(default=1, description="Version number of the template")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when template was created",
    )

    @model_validator(mode="after")
    def validate_placeholders(self) -> "Template":
        """Validate that template placeholders match template_text."""
        is_valid, errors = PlaceholderParser.validate_placeholders(
            self.template_text, self.placeholders
        )
        if not is_valid:
            raise ValueError(
                f"Template '{self.id}' validation failed: {'; '.join(errors)}"
            )
        return self
