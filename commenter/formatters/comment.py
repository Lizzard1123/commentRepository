from datetime import datetime
import random
import string
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

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
        Parse the AI inference XML output into structured components.

        Args:
            inference_output (str): AI-generated XML string.

        Returns:
            Dict: Structured representation of the function details.
        """
        result = {"name": "", "description": "", "parameters": [], "returns": {}}

        try:
            root = ET.fromstring(inference_output)

            result["name"] = root.findtext("name", "").strip()
            result["description"] = root.findtext("description", "").strip()

            # Extract parameters
            parameters = root.find("parameters")
            if parameters is not None:
                for param in parameters.findall("param"):
                    param_data = {
                        "name": param.findtext("name", "").strip(),
                        "type": param.findtext("type", "").strip(),
                        "description": param.findtext("description", "").strip()
                    }
                    result["parameters"].append(param_data)

            # Extract return value
            returns = root.find("returns")
            if returns is not None:
                result["returns"] = {
                    "type": returns.findtext("type", "").strip(),
                    "description": returns.findtext("description", "").strip()
                }

        except ET.ParseError as e:
            print(f"XML Parsing Error: {e}")

        return result

    def format_comment(
        self, inference_output: str, previous_comment: Optional[str] = None, metadata: dict = None
    ) -> str:
        """
        Format the inference output into a TypeScript comment with metadata, maintaining versioning.

        Args:
            inference_output (str): Raw output from the inference service
            previous_comment (Optional[str]): The previous comment for version tracking
            metadata (dict): Metadata about the TypeScript element

        Returns:
            str: Formatted TypeScript comment
        """
        parsed = self._parse_inference_output(inference_output)
        slug = self._generate_slug()

        # Extract previous version if available
        version = "v1.0"
        if previous_comment:
            import re
            match = re.search(r'@generated\s+\w+\s+(v\d+\.\d+)', previous_comment)
            if match:
                prev_version = match.group(1)
                major, minor = map(int, prev_version[1:].split("."))
                version = f"v{major}.{minor + 1}"

        comment_lines = ["/**"]
        comment_lines.append(f' * {parsed["description"]}')
        comment_lines.append(" *")

        # Add parameters if applicable
        if parsed["parameters"]:
            for param in parsed["parameters"]:
                comment_lines.append(f' * @param {param["name"]} {{{param["type"]}}} {param["description"]}')
            comment_lines.append(" *")

        # Include return type only for functions
        if metadata and metadata.get("type") == "function" and parsed["returns"].get("type") != "void":
            return_type = parsed["returns"].get("type", "").strip()
            return_desc = parsed["returns"].get("description", "").strip()
            if return_type:
                comment_lines.append(f' * @returns {{ {return_type} }} {return_desc}')
                comment_lines.append(" *")

        # Indicate if the function is async
        if metadata and metadata.get("isAsync"):
            comment_lines.append(" * @async")
            comment_lines.append(" *")

        # Add metadata with versioning
        comment_lines.append(
            f" * @generated {slug} {version} Generated on: {self._format_date()} by {self.model_name}"
        )
        comment_lines.append(" */")

        return "\n".join(comment_lines)

    def create_prompt(self, code: str, context: Optional[str] = None) -> str:
        """
        Create a standardized prompt for inference services using XML format.

        Args:
            code (str): The TypeScript code to analyze
            context (Optional[str]): Additional context about the code

        Returns:
            str: Formatted prompt
        """
        return f"""Analyze the following TypeScript element and generate a structured XML response with the following format:
        
        <element>
            <name>element_name</name>
            <description>Brief description of what this element does.</description>
            <type>element_type (e.g., function, class, interface, type, etc.)</type>
            <isAsync>true/false (only if applicable)</isAsync>
            <parameters>
                <param>
                    <name>param_name</name>
                    <type>param_type</type>
                    <description>Detailed description of the parameter.</description>
                </param>
                ...
            </parameters>
            <returns>
                <type>return_type (omit if not a function)</type>
                <description>Detailed description of the return value.</description>
            </returns>
        </element>

        Context:
        {context if context else 'No additional context provided'}

        Code:
        {code}

        Please return only the XML response without any additional formatting or explanations."""
