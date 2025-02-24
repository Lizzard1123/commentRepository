from typing import Optional
import anthropic
from ..models.base import InferenceBase


class ClaudeInference(InferenceBase):
    """Claude API implementation for code commenting."""

    def __init__(self, api_key: str):
        """
        Initialize Claude client.

        Args:
            api_key (str): Anthropic API key
        """
        self.client = anthropic.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text
