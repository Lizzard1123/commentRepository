import os
from ..models.base import InferenceBase
from ..formatters.readme import ReadmeFormatter
from termcolor import colored

def process_readme(
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
