from datetime import datetime
import random
import string
from typing import Dict, List, Optional


class CommentFormatter:
    """Formats comments for TypeScript code with consistent structure and metadata."""

    def __init__(self, model_name: str):
        """
        Initialize the formatter with the model name.

        Args:
            model_name (str): Name of the model used for generation
        """
        self.model_name = model_name

    def _generate_slug(self) -> str:
        """Generate a 6-character alphanumeric slug."""
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(6))

    def _format_date(self) -> str:
        """Get current date in yyyy-MM-dd HH:mm:ss format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _parse_inference_output(self, inference_output: str) -> Dict:
        """
        Parse the raw inference output into structured components.
        Expected format from inference:
        - Name: <function name>
        - Description: <description>
        - Parameters:
          - param1: <description> [default: <value>]
          - param2: <description>
        - Returns: <return description>
        """
        # This is a simple parser - you might want to make it more robust
        lines = inference_output.strip().split("\n")
        result = {"name": "", "description": "", "parameters": [], "returns": ""}

        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith("Name:"):
                result["name"] = line[5:].strip()
                current_section = "name"
            elif line.startswith("Description:"):
                result["description"] = line[12:].strip()
                current_section = "description"
            elif line.startswith("Parameters:"):
                current_section = "parameters"
            elif line.startswith("Returns:"):
                result["returns"] = line[8:].strip()
                current_section = "returns"
            elif line.startswith("-") and current_section == "parameters":
                param_line = line[1:].strip()
                param_parts = param_line.split(":")
                param_name = param_parts[0].strip()
                param_desc = ":".join(param_parts[1:]).strip()

                # Check for default value
                default_value = None
                if "[default:" in param_desc:
                    desc_parts = param_desc.split("[default:")
                    param_desc = desc_parts[0].strip()
                    default_value = desc_parts[1].strip("]").strip()

                result["parameters"].append(
                    {
                        "name": param_name,
                        "description": param_desc,
                        "default": default_value,
                    }
                )
            elif line and current_section:
                # Append to current section for multi-line descriptions
                if current_section == "description":
                    result["description"] += " " + line
                elif current_section == "returns":
                    result["returns"] += " " + line

        return result

    def format_comment(self, inference_output: str) -> str:
        """
        Format the inference output into a TypeScript comment with metadata.

        Args:
            inference_output (str): Raw output from the inference service

        Returns:
            str: Formatted TypeScript comment
        """
        parsed = self._parse_inference_output(inference_output)
        slug = self._generate_slug()

        comment_lines = ["/**"]
        comment_lines.append(f' * {parsed["description"]}')
        comment_lines.append(" *")

        # Add parameters
        if parsed["parameters"]:
            for param in parsed["parameters"]:
                param_line = f' * @param {param["name"]} {param["description"]}'
                if param["default"]:
                    param_line += f' (default: {param["default"]})'
                comment_lines.append(param_line)
            comment_lines.append(" *")

        # Add return value
        if parsed["returns"]:
            comment_lines.append(f' * @returns {parsed["returns"]}')
            comment_lines.append(" *")

        # Add metadata
        comment_lines.append(
            f" * @generated {slug} Generated on: {self._format_date()} by {self.model_name}"
        )
        comment_lines.append(" */")

        return "\n".join(comment_lines)

    def create_prompt(self, code: str, context: Optional[str] = None) -> str:
        """
        Create a standardized prompt for inference services.

        Args:
            code (str): The TypeScript code to analyze
            context (Optional[str]): Additional context about the code

        Returns:
            str: Formatted prompt
        """
        return f"""Please analyze this TypeScript code and provide a structured response with the following sections:
        - Name: The function name
        - Description: A clear, concise description of what the function does
        - Parameters: List each parameter with its description and default value (if any)
        - Returns: Description of the return value

        Code:
        {code}

        Additional Context:
        {context if context else 'No additional context provided'}

        Please provide only the structured information without any additional formatting or explanations."""
