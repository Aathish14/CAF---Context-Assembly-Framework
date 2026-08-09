"""Context model for CAF application."""

from pydantic import BaseModel, Field


class Context(BaseModel):
    """Context model representing the context for content generation."""

    objective: str = Field(..., description="The objective of the content generation")
    audience: str = Field(..., description="The target audience for the content")
    tone: str = Field(..., description="The tone to use for the content")
    constraints: list[str] = Field(
        default_factory=list, description="List of constraints for the content"
    )
    output_format: str = Field(..., description="The desired output format")
    risk_level: str = Field(
        ..., description="The risk level associated with the content"
    )
    language: str = Field(..., description="The language for the content")
    word_limit: int | None = Field(
        default=None, description="Optional word limit for the content"
    )
    purpose: str = Field(..., description="The purpose of the content generation")
    business_type: str = Field(..., description="The type of business for the content")
