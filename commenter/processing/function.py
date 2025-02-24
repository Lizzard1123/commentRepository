import os
from ..models.base import InferenceBase
from ..formatters.comment import CommentFormatter
from ..parsers.typescript import TypeScriptParser
from termcolor import colored

def process_functions(
    inference: InferenceBase, formatter: CommentFormatter, file_path: str
):
    """Extracts and updates function comments in a TypeScript file using AI inference."""
    parser = TypeScriptParser()
    print(colored(f"Parsing file: {file_path}", "magenta"))

    # Read current file content
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
        print(colored(f"Processing function: {func_name}", "cyan"))

        # Remove old comment if present
        start_line = metadata["pos"]["startLine"] - 1 + insertion_offsets
        while start_line > 0 and (updated_lines[start_line - 1].strip().startswith("/*") or updated_lines[start_line - 1].strip().startswith("*")):
            del updated_lines[start_line - 1]
            start_line -= 1
            insertion_offsets -= 1

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

        # Get the indentation of the function
        function_line = updated_lines[start_line]
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
        updated_lines[start_line:start_line] = comment_lines
        insertion_offsets += len(comment_lines)

    # Write the modified content back to the file
    with open(file_path, "w") as f:
        f.writelines(updated_lines)

    print(colored(f"Finished processing {file_path}", "green"))
