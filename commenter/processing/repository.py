import os
from ..models.base import InferenceBase
from ..formatters.comment import CommentFormatter
from .function import process_file
from termcolor import colored

def process_repository(inference: InferenceBase, formatter: CommentFormatter, repo_path: str):
    """Recursively process all TypeScript files in a repository for function documentation."""
    print(colored(f"Processing repository: {repo_path}", "yellow"))
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".ts"):
                file_path = os.path.join(root, file)
                print(colored(f"Processing file: {file_path}", "blue"))
                process_file(inference, formatter, file_path)
