from abc import ABC, abstractmethod
from typing import Optional


class InferenceBase(ABC):
    """Base class for AI inference implementations."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response via a LLM

        Args:
            code (str): The question

        Returns:
            str: Generated text
        """
        pass
