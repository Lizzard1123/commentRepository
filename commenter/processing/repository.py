import os
import time
from ..models.base import InferenceBase
from ..formatters.comment import CommentFormatter
from ..formatters.readme import ReadmeFormatter
from .function import process_file
from .readme import process_readme
from termcolor import colored


def process_repository(
    inference: InferenceBase, comment_formatter: CommentFormatter, readme_formatter: ReadmeFormatter, repo_path: str
):
    """Recursively process all eligible files in a repository, generating READMEs bottom-up."""
    EXCLUDED_DIRS = {"node_modules", "dist", "build", "venv", "__pycache__"}
    ELIGIBLE_EXTENSIONS = {".ts", ".tsx"}

    print(colored(f"Scanning repository: {repo_path}", "yellow"))
    all_files = []
    all_dirs = set()

    # First pass: Collect eligible files and directories
    for root, dirs, files in os.walk(repo_path, topdown=True):
        dirs[:] = [
            d for d in dirs if d not in EXCLUDED_DIRS
        ]  # Exclude specified directories
        eligible_files = [
            os.path.join(root, f)
            for f in files
            if os.path.splitext(f)[1] in ELIGIBLE_EXTENSIONS
        ]

        if eligible_files:
            all_files.extend(eligible_files)
            all_dirs.add(root)

    total_tasks = len(all_files) + len(all_dirs)  # Total progress count
    completed_tasks = 0
    start_time = time.time()

    # Process each file
    for file_path in all_files:
        print(colored(f"Processing file: {file_path}", "blue"))
        process_file(inference, comment_formatter, file_path)
        completed_tasks += 1
        show_progress(completed_tasks, total_tasks, start_time)

    # Process directories bottom-up for README generation
    for directory in sorted(all_dirs, key=lambda d: d.count(os.sep), reverse=True):
        print(colored(f"Generating README for directory: {directory}", "green"))
        process_readme(inference, readme_formatter, directory)
        completed_tasks += 1
        show_progress(completed_tasks, total_tasks, start_time)

    print(colored("Repository processing complete!", "cyan"))


def show_progress(completed, total, start_time):
    """Displays a progress bar with estimated time remaining."""
    elapsed_time = time.time() - start_time
    progress = completed / total
    estimated_total_time = elapsed_time / progress if progress > 0 else 0
    remaining_time = estimated_total_time - elapsed_time

    bar_length = 40
    filled_length = int(bar_length * progress)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)

    print(
        colored(
            f"[{bar}] {completed}/{total} tasks completed. Estimated time left: {remaining_time:.2f}s",
            "magenta",
        )
    )
