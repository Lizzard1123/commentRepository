from typing import Optional
import requests
from ..models.base import InferenceBase


class OllamaInference(InferenceBase):
    """Ollama implementation for code commenting."""

    def __init__(self, host: str = "http://localhost:11434"):
        """
        Initialize Ollama client.

        Args:
            host (str): Ollama API host address
        """
        self.host = host

    def generate_comment(self, code: str, context: Optional[str] = None) -> str:
        prompt = f"""Please provide a comprehensive comment for the following code.
        If context is provided, incorporate it into the comment.

        Code:
        {code}

        Context:
        {context if context else 'No additional context provided'}
        """

        response = requests.post(
            f"{self.host}/api/generate",
            json={"model": "codellama", "prompt": prompt, "stream": False},
        )

        return response.json()["response"]
