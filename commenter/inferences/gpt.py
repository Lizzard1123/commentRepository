from typing import Optional
import openai
from ..models.base import InferenceBase


class GPTInference(InferenceBase):
    """OpenAI GPT implementation for code commenting."""

    def __init__(self, api_key: str):
        """
        Initialize OpenAI client.

        Args:
            api_key (str): OpenAI API key
        """
        openai.api_key = api_key

    def generate_comment(self, code: str, context: Optional[str] = None) -> str:
        prompt = f"""Please provide a comprehensive comment for the following code.
        If context is provided, incorporate it into the comment.

        Code:
        {code}

        Context:
        {context if context else 'No additional context provided'}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
