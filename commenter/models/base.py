from abc import ABC, abstractmethod
from typing import Optional


class InferenceBase(ABC):
    """Base class for AI inference implementations."""

    @abstractmethod
    def generate_comment(self, code: str, context: Optional[str] = None) -> str:
        """
        Generate a comment for the given code snippet.

        Args:
            code (str): The code to comment
            context (Optional[str]): Additional context about the code

        Returns:
            str: Generated comment
        """
        pass
