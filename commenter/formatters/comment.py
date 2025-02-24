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
        lines = inference_output.strip().split("\n")
        result = {"name": "", "description": "", "parameters": [], "returns": ""}

        current_section = None

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Handle main sections
            if line.startswith("- Name:"):
                current_section = "name"
                result["name"] = line.replace("- Name:", "").strip()
            elif line.startswith("- Description:"):
                current_section = "description"
                result["description"] = line.replace("- Description:", "").strip()
            elif line.startswith("- Parameters:"):
                current_section = "parameters"
                buffer = []  # Reset buffer for parameters
            elif line.startswith("- Returns:"):
                current_section = "returns"
                result["returns"] = line.replace("- Returns:", "").strip()
            # Handle parameter entries
            elif line.startswith("  -") and current_section == "parameters":
                param_line = line.replace("  -", "").strip()

                # Split on first colon to separate name and description
                param_parts = param_line.split(":", 1)
                if len(param_parts) == 2:
                    param_name = param_parts[0].strip()
                    param_desc = param_parts[1].strip()

                    # Parse type information if present
                    param_type = None
                    if "," in param_desc:
                        type_parts = param_desc.split(",", 1)
                        param_type = type_parts[0].strip()
                        param_desc = type_parts[1].strip()

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
                            "type": param_type,
                            "default": default_value,
                        }
                    )
            # Append to current section for multi-line content
            elif current_section and not line.startswith("-"):
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
