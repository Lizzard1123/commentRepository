import os
from ..models.base import InferenceBase
from ..formatters.comment import CommentFormatter
from ..parsers.typescript import TypeScriptParser
from termcolor import colored

def process_element(
    inference: InferenceBase,
    formatter: CommentFormatter,
    file_path: str,
    slug: str,
):
    """Processes an element (function, interface, class, type, etc.) in a TypeScript file by adding/updating its comment using the provided slug."""
    parser = TypeScriptParser()

    # Read file content
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parse elements from file
    elements = parser.parse_file(file_path)

    for name, element_code, metadata in elements:
        comment_slug = extract_slug_from_comment(
            lines, metadata.get("pos", {}).get("startLine", 1) - 1
        )
        if comment_slug != slug:
            continue

        updated_lines, insertion_offsets = insert_comment(
            inference, formatter, file_path, lines, name, element_code, metadata
        )

        # Write updated content back to the file
        with open(file_path, "w") as f:
            f.writelines(updated_lines)

        print(colored(f"Processed element with slug: {slug} in {file_path}", "green"))
        return

    print(colored(f"Element with slug {slug} not found in {file_path}", "red"))

def extract_slug_from_comment(lines, start_line):
    """Extracts the slug from the comment above an element."""
    for i in range(start_line - 1, -1, -1):
        line = lines[i].strip()
        if "@generated" in line:
            parts = line.split()
            for part in parts:
                if len(part) == 6 and part.isalnum():
                    return part
    return None

def process_file(inference: InferenceBase, formatter: CommentFormatter, file_path: str):
    """Processes all elements in a TypeScript file by adding/updating comments."""
    parser = TypeScriptParser()

    # Read file content
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parse elements from file
    elements = parser.parse_file(file_path)
    if not elements:
        print(colored(f"No elements found in {file_path}", "red"))
        return

    updated_lines = lines[:]
    insertion_offsets = 0

    for element_name, element_code, metadata in elements:
        updated_lines, insertion_offsets = insert_comment(
            inference,
            formatter,
            file_path,
            updated_lines,
            element_name,
            element_code,
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
    element_name,
    element_code,
    metadata,
    insertion_offsets=0,
):
    """Inserts or updates a comment for a given element (function, class, interface, type, etc.)."""
    print(colored(f"Processing element: {element_name}", "cyan"))

    start_line = metadata.get("pos", {}).get("startLine", 1) - 1 + insertion_offsets
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
        f"{param.get('name', 'unknown')}: {param.get('type', 'unknown')}"
        for param in metadata.get("parameters", [])
    ]
    params_str = ", ".join(param_strings)

    module_context = f"File: {os.path.basename(file_path)}"
    context = (
        f"{module_context}\n"
        f"Element: {element_name}\n"
        f"Type: {metadata.get('type', 'unknown')}\n"
        f"Return Type: {metadata.get('returnType', 'unknown')}\n"
        f"Is Async: {metadata.get('isAsync', False)}\n"
        f"Parameters: {params_str}"
        f"\nStart Line: {metadata.get('pos', {}).get('startLine', 'unknown')}\n"
        f"End Line: {metadata.get('pos', {}).get('endLine', 'unknown')}"
    )

    prompt = formatter.create_prompt(element_code, context=context)
    raw_comment = inference.generate(prompt)
    formatted_comment = formatter.format_comment(raw_comment, previous_comment_text, metadata)

    # Detect indentation level from element line
    element_line = lines[start_line]
    indentation = element_line[: len(element_line) - len(element_line.lstrip())]

    # Apply detected indentation to each line of the comment
    comment_lines = [(indentation + line).rstrip() + "\n" for line in formatted_comment.split("\n")]

    lines[start_line:start_line] = comment_lines
    insertion_offsets += len(comment_lines)

    return lines, insertion_offsets
