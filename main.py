import click
import os
from typing import Optional
from commenter.inferences.claude import ClaudeInference
from commenter.inferences.gpt import GPTInference
from commenter.inferences.ollama import OllamaInference
from commenter.models.base import InferenceBase


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

    # Initialize the appropriate inference service
    if service == "claude":
        if not api_key:
            raise click.BadParameter("API key required for Claude service")
        inference = ClaudeInference(api_key)
    elif service == "gpt":
        if not api_key:
            raise click.BadParameter("API key required for GPT service")
        inference = GPTInference(api_key)
    else:  # ollama
        inference = OllamaInference()

    if type == "repository":
        process_repository(inference, input_path)
    elif type == "functions":
        process_functions(inference, input_path)
    else:  # readme
        generate_readme(inference, input_path)


def process_repository(inference: InferenceBase, repo_path: str):
    """Process all Python files in a repository."""
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                process_functions(inference, file_path)


def process_functions(inference: InferenceBase, file_path: str):
    """Process individual functions in a Python file."""
    import ast

    with open(file_path, "r") as f:
        content = f.read()

    tree = ast.parse(content)

    # Collect context about the module
    module_context = f"File: {os.path.basename(file_path)}"

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Extract the function source code
            function_code = ast.get_source_segment(content, node)

            # Generate comment
            comment = inference.generate_comment(
                function_code, context=f"{module_context}\nFunction: {node.name}"
            )

            print(f"\nProcessing function: {node.name}")
            print("Generated comment:")
            print(comment)


def generate_readme(inference: InferenceBase, repo_path: str):
    """Generate a README.md file for the repository."""
    # Collect repository information
    repo_name = os.path.basename(os.path.abspath(repo_path))

    # Generate content for README
    content = f"""
    Repository: {repo_name}

    This is an automated analysis of the repository structure and contents.
    """

    comment = inference.generate_comment(
        content, context=f"Generate a README.md file for repository: {repo_name}"
    )

    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(comment)

    print(f"\nGenerated README.md at: {readme_path}")


if __name__ == "__main__":
    main()
