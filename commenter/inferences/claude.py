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

    def generate_comment(self, code: str, context: Optional[str] = None) -> str:
        prompt = f"""Please provide a comprehensive comment for the following code.
        If context is provided, incorporate it into the comment.

        Code:
        {code}

        Context:
        {context if context else 'No additional context provided'}
        """

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text
