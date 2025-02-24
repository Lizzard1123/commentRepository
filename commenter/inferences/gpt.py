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

    def generate(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
