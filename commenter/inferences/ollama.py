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

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.host}/api/generate",
            json={"model": "qwen2.5:7b-instruct", "prompt": prompt, "stream": False},
        )

        return response.json()["response"]
