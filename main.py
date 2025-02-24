import click
import os
from typing import Optional
from commenter.inferences.claude import ClaudeInference
from commenter.inferences.gpt import GPTInference
from commenter.inferences.ollama import OllamaInference
from commenter.models.base import InferenceBase
from commenter.formatters.comment import CommentFormatter
from commenter.formatters.readme import ReadmeFormatter
from commenter.parsers.typescript import TypeScriptParser


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
        model_name = "Claude"
    elif service == "gpt":
        if not api_key:
            raise click.BadParameter("API key required for GPT service")
        inference = GPTInference(api_key)
        model_name = "GPT-4"
    else:  # ollama
        inference = OllamaInference()
        model_name = "Ollama"

    # Initialize formatters
    comment_formatter = CommentFormatter(model_name)
    readme_formatter = ReadmeFormatter(model_name)

    if type == "repository":
        process_repository(inference, comment_formatter, input_path)
    elif type == "functions":
        process_functions(inference, comment_formatter, input_path)
    else:  # readme
        generate_readme(inference, readme_formatter, input_path)


def process_repository(inference: InferenceBase, formatter: CommentFormatter, repo_path: str):
    """Process all TypeScript files in a repository."""
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".ts"):
                file_path = os.path.join(root, file)
                process_functions(inference, formatter, file_path)


def process_functions(
    inference: InferenceBase, formatter: CommentFormatter, file_path: str
):
    """Process all functions in a TypeScript file."""
    parser = TypeScriptParser()

    # Read current file content
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parse functions from file
    functions = parser.parse_file(file_path)
    if not functions:
        return

    updated_lines = lines[:]
    insertion_offsets = 0

    for func_name, func_code, metadata in functions:
        # Format parameters as a string
        param_strings = [f"{param['name']}: {param['type']}" for param in metadata["parameters"]]
        params_str = ", ".join(param_strings)

        # Create context with TypeScript-specific information
        module_context = f"File: {os.path.basename(file_path)}"
        context = (
            f"{module_context}\n"
            f"Function: {func_name}\n"
            f"Return Type: {metadata['returnType']}\n"
            f"Is Async: {metadata['isAsync']}\n"
            f"Parameters: {params_str}"
        )

        # Create prompt and get inference
        prompt = formatter.create_prompt(func_code, context=context)
        raw_comment = inference.generate_comment(prompt)

        # Format the comment
        formatted_comment = formatter.format_comment(raw_comment)

        # Determine insertion position
        insert_position = metadata["pos"]["startLine"] - 1 + insertion_offsets

        # Get the indentation of the function
        function_line = updated_lines[insert_position]
        indentation = ""
        for char in function_line:
            if char in [" ", "\t"]:
                indentation += char
            else:
                break

        # Add indentation to each comment line
        comment_lines = [
            indentation + line + "\n" for line in formatted_comment.split("\n")
        ]

        # Insert the comment lines before the function
        updated_lines[insert_position:insert_position] = comment_lines
        insertion_offsets += len(comment_lines)

    # Write the modified content back to the file
    with open(file_path, "w") as f:
        f.writelines(updated_lines)

    print(f"\nFinished processing {file_path}")


def generate_readme(
    inference: InferenceBase, formatter: ReadmeFormatter, repo_path: str
):
    """Generate a README.md file for the repository."""
    # Collect repository information
    repo_name = os.path.basename(os.path.abspath(repo_path))

    # Create prompt and get inference
    prompt = formatter.create_prompt(repo_path)
    raw_content = inference.generate_comment(prompt)

    # Format the README
    formatted_content = formatter.format_readme(raw_content, repo_name)

    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(formatted_content)

    print(f"\nGenerated README.md at: {readme_path}")


if __name__ == "__main__":
    main()
