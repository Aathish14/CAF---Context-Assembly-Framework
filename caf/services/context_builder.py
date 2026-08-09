"""Context builder service for CAF application."""

from caf.models.context import Context


class ContextBuilder:
    """Builds Context objects from validated user answers."""

    def build(self, answers: dict) -> Context:
        """Build a Context object from validated answers.

        Args:
            answers: Dictionary of validated user answers.

        Returns:
            Context: Constructed Context instance.

        Raises:
            ValueError: If Context creation fails due to missing required fields.
        """
        # Make a copy to avoid modifying the original dict
        processed_answers = answers.copy()
        
        # Convert constraints from comma-separated string to list
        if "constraints" in processed_answers and isinstance(
            processed_answers["constraints"], str
        ):
            constraints_str = processed_answers["constraints"]
            if constraints_str.strip() == "":
                processed_answers["constraints"] = []
            else:
                # Split by comma, strip whitespace, and filter out empty strings
                processed_answers["constraints"] = [
                    c.strip() for c in constraints_str.split(",") if c.strip()
                ]
        
        # Convert word_limit from string to integer if possible
        if "word_limit" in processed_answers and isinstance(
            processed_answers["word_limit"], str
        ):
            word_limit_str = processed_answers["word_limit"]
            if word_limit_str.strip() == "":
                processed_answers["word_limit"] = None
            else:
                # Try to convert to integer - let ValueError propagate if invalid
                processed_answers["word_limit"] = int(word_limit_str)
        
        return Context(**processed_answers)
