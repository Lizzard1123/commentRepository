import click
import os
import sys
from typing import Optional
from commenter.inferences.claude import ClaudeInference
from commenter.inferences.gpt import GPTInference
from commenter.inferences.ollama import OllamaInference
from commenter.models.base import InferenceBase
from commenter.formatters.comment import CommentFormatter
from commenter.formatters.readme import ReadmeFormatter
from commenter.processing.function import process_function, process_file
from commenter.processing.readme import process_readme
from commenter.processing.repository import process_repository
from termcolor import colored

@click.command()
@click.option(
    "--type",
    type=click.Choice(["repository", "functions", "readme", "slug"]),
    required=True,
    help="Type of documentation to generate",
)
@click.option(
    "--service",
    type=click.Choice(["claude", "gpt", "ollama"]),
    required=True,
    help="AI service to use",
)
@click.option("--api-key", help="API key for Claude or GPT services", required=False)
@click.option("--input-path", required=True, help="Path to code file or directory")
@click.option("--slug-code", required=False, help="Function slug to document (required if type is 'slug')")

def main(type: str, service: str, api_key: Optional[str], input_path: str, slug_code: Optional[str]):
    """Generate code comments using AI services."""
    print(colored(f"Initializing documentation generation for {type}...", "cyan"))

    # Initialize the appropriate inference service
    if service == "claude":
        if not api_key:
            print(colored("API key required for Claude service", "red"))
            sys.exit(1)
        inference = ClaudeInference(api_key)
        model_name = "Claude"
    elif service == "gpt":
        if not api_key:
            print(colored("API key required for GPT service", "red"))
            sys.exit(1)
        inference = GPTInference(api_key)
        model_name = "GPT-4"
    else:  # ollama
        inference = OllamaInference()
        model_name = "Ollama"

    print(colored(f"Using {model_name} model for inference.", "green"))

    # Initialize formatters
    comment_formatter = CommentFormatter(model_name)
    readme_formatter = ReadmeFormatter(model_name)

    if type == "repository":
        process_repository(inference, comment_formatter, input_path)
    elif type == "functions":
        process_file(inference, comment_formatter, input_path)
    elif type == "slug":
        if not slug_code:
            print(colored("Error: --slug-code is required when type is 'slug'", "red"))
            sys.exit(1)
        process_function(inference, comment_formatter, input_path, slug_code)
    else:  # readme
        process_readme(inference, readme_formatter, input_path)

if __name__ == "__main__":
    main()
