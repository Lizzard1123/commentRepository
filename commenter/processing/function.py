import os
from ..models.base import InferenceBase
from ..formatters.comment import CommentFormatter
from ..parsers.typescript import TypeScriptParser
from termcolor import colored


def process_function(
    inference: InferenceBase,
    formatter: CommentFormatter,
    file_path: str,
    func_slug: str,
):
    """Processes a single function in a TypeScript file by adding/updating its comment using the function slug."""
    parser = TypeScriptParser()

    # Read file content
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parse functions from file
    functions = parser.parse_file(file_path)

    for name, func_code, metadata in functions:
        comment_slug = extract_slug_from_comment(
            lines, metadata["pos"]["startLine"] - 1
        )
        if comment_slug != func_slug:
            continue

        updated_lines, insertion_offsets = insert_comment(
            inference, formatter, file_path, lines, name, func_code, metadata
        )

        # Write updated content back to the file
        with open(file_path, "w") as f:
            f.writelines(updated_lines)

        print(
            colored(
                f"Processed function with slug: {func_slug} in {file_path}", "green"
            )
        )
        return

    print(colored(f"Function with slug {func_slug} not found in {file_path}", "red"))


def extract_slug_from_comment(lines, start_line):
    """Extracts the slug from the comment above the function."""
    for i in range(start_line - 1, -1, -1):
        line = lines[i].strip()
        if "@generated" in line:
            parts = line.split()
            for part in parts:
                if len(part) == 6 and part.isalnum():
                    return part
    return None


def process_file(inference: InferenceBase, formatter: CommentFormatter, file_path: str):
    """Processes all functions in a TypeScript file by adding/updating comments."""
    parser = TypeScriptParser()

    # Read file content
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parse functions from file
    functions = parser.parse_file(file_path)
    if not functions:
        print(colored(f"No functions found in {file_path}", "red"))
        return

    updated_lines = lines[:]
    insertion_offsets = 0

    for func_name, func_code, metadata in functions:
        updated_lines, insertion_offsets = insert_comment(
            inference,
            formatter,
            file_path,
            updated_lines,
            func_name,
            func_code,
            metadata,
            insertion_offsets,
        )

    # Write updated content back to the file
    with open(file_path, "w") as f:
        f.writelines(updated_lines)

    print(colored(f"Finished processing {file_path}", "green"))

def insert_comment(
    inference,
    formatter,
    file_path,
    lines,
    func_name,
    func_code,
    metadata,
    insertion_offsets=0,
):
    """Inserts or updates a comment for a given function."""
    print(colored(f"Processing function: {func_name}", "cyan"))

    start_line = metadata["pos"]["startLine"] - 1 + insertion_offsets
    previous_comment = []
    comment_start = start_line - 1

    while comment_start >= 0 and (
        lines[comment_start].strip().startswith("/*")
        or lines[comment_start].strip().startswith("*")
    ):
        previous_comment.insert(0, lines[comment_start])
        del lines[comment_start]
        start_line -= 1
        insertion_offsets -= 1
        comment_start -= 1

    previous_comment_text = "".join(previous_comment) if previous_comment else None

    param_strings = [
        f"{param['name']}: {param['type']}" for param in metadata["parameters"]
    ]
    params_str = ", ".join(param_strings)

    module_context = f"File: {os.path.basename(file_path)}"
    context = (
        f"{module_context}\n"
        f"Function: {func_name}\n"
        f"Return Type: {metadata['returnType']}\n"
        f"Is Async: {metadata['isAsync']}\n"
        f"Parameters: {params_str}"
    )

    prompt = formatter.create_prompt(func_code, context=context)
    raw_comment = inference.generate_comment(prompt)
    formatted_comment = formatter.format_comment(raw_comment, previous_comment_text)

    # Detect indentation level from function line
    function_line = lines[start_line]
    indentation = function_line[: len(function_line) - len(function_line.lstrip())]

    # Apply detected indentation to each line of the comment
    comment_lines = [(indentation + line).rstrip() + "\n" for line in formatted_comment.split("\n")]

    lines[start_line:start_line] = comment_lines
    insertion_offsets += len(comment_lines)

    return lines, insertion_offsets
