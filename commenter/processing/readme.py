import os
import subprocess
from ..models.base import InferenceBase
from ..formatters.readme import ReadmeFormatter
from termcolor import colored


def process_readme(
    inference: InferenceBase, formatter: ReadmeFormatter, repo_path: str
):
    """Creates a structured README.md file for the given repository."""

    print(colored(f"📂 Scanning repository: {repo_path}", "cyan"))

    readme_path = os.path.join(repo_path, "README.md")
    if os.path.exists(readme_path):
        os.remove(readme_path)
        print(colored("🗑️ Removed existing README.md", "red"))

    repo_name = os.path.basename(os.path.abspath(repo_path))
    tree_structure = _get_repo_tree(repo_path)

    file_summaries = _summarize_files(inference, repo_path)
    folder_summaries = _summarize_folders(inference, repo_path, file_summaries)

    full_summary = _summarize_repository(inference, repo_name, folder_summaries)

    formatted_content = formatter.format_readme(
        full_summary, repo_name, tree_structure, folder_summaries
    )

    with open(readme_path, "w") as f:
        f.write(formatted_content)

    print(colored(f"✅ Generated new README.md at: {readme_path}", "green"))


def _get_repo_tree(repo_path: str) -> str:
    """Get the directory structure of the repository using the 'tree' command."""
    print(colored("📌 Generating project structure...", "yellow"))
    try:
        return subprocess.check_output(
            ["tree", "-I", "node_modules"], cwd=repo_path, text=True
        )
    except FileNotFoundError:
        print(colored("⚠️ Tree command not found. Please install it.", "red"))
        return "Tree command not available."


def _summarize_files(inference: InferenceBase, repo_path: str) -> dict:
    """Generate summaries for individual files in the repository."""
    file_summaries = {}

    print(colored("📄 Summarizing files...", "blue"))
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                print(colored(f"🔍 Processing file: {file_path}", "magenta"))
                summary = inference.generate_comment(
                    f"Summarize this file. Only include code snippets if absolutely necessary:\n\n{content}"
                )
                file_summaries[file_path] = summary

            except Exception as e:
                print(colored(f"⚠️ Skipping {file_path} due to error: {e}", "red"))

    print(colored("✅ Completed file summaries.", "green"))
    return file_summaries


def _summarize_folders(
    inference: InferenceBase, repo_path: str, file_summaries: dict
) -> dict:
    """Generate summaries for folders, using file summaries first before summarizing subfolders."""
    folder_summaries = {}

    print(colored("📁 Summarizing folders...", "blue"))
    for root, dirs, _ in os.walk(repo_path, topdown=False):
        content_summaries = [
            file_summaries[path] for path in file_summaries if path.startswith(root)
        ]

        if not content_summaries:
            continue

        context = "\n".join(content_summaries)
        print(colored(f"📦 Processing folder: {root}", "magenta"))
        folder_summary = inference.generate_comment(
            f"Summarize the purpose of this folder based on its files:\n{context}"
        )

        folder_summaries[root] = folder_summary

    print(colored("✅ Completed folder summaries.", "green"))
    return folder_summaries


def _summarize_repository(
    inference: InferenceBase, repo_name: str, folder_summaries: dict
) -> str:
    """Generate the final repository summary based on the folder summaries."""
    full_context = "\n".join(folder_summaries.values())

    print(colored("📝 Generating final repository summary...", "yellow"))
    summary = inference.generate_comment(
        f"Summarize the repository '{repo_name}' based on the following folder summaries. Only include code snippets if they are crucial:\n{full_context}"
    )

    print(colored("✅ Repository summary generated.", "green"))
    return summary
