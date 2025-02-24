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
from commenter.processing.function import process_functions
from commenter.processing.readme import process_readme
from commenter.processing.repository import process_repository
from termcolor import colored

@click.command()
@click.option(
    "--type",
    type=click.Choice(["repository", "functions", "readme"]),
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
def main(type: str, service: str, api_key: Optional[str], input_path: str):
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
        process_functions(inference, comment_formatter, input_path)
    else:  # readme
        process_readme(inference, readme_formatter, input_path)

def process_repository(inference: InferenceBase, formatter: CommentFormatter, repo_path: str):
    """Recursively process all TypeScript files in a repository for function documentation."""
    print(colored(f"Processing repository: {repo_path}", "yellow"))
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".ts"):
                file_path = os.path.join(root, file)
                print(colored(f"Processing file: {file_path}", "blue"))
                process_functions(inference, formatter, file_path)


def generate_readme(
    inference: InferenceBase, formatter: ReadmeFormatter, repo_path: str
):
    """Creates a structured README.md file for the given repository."""
    print(colored(f"Generating README for {repo_path}", "yellow"))
    
    repo_name = os.path.basename(os.path.abspath(repo_path))
    prompt = formatter.create_prompt(repo_path)
    raw_content = inference.generate_comment(prompt)
    formatted_content = formatter.format_readme(raw_content, repo_name)

    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(formatted_content)

    print(colored(f"Generated README.md at: {readme_path}", "green"))

if __name__ == "__main__":
    main()
