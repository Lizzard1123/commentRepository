import os
from typing import List, Tuple
import subprocess
import json
import tempfile


class TypeScriptParser:
    """Parser for TypeScript files to extract function information."""

    @staticmethod
    def _create_ast_generator_script() -> str:
        """Create a temporary TypeScript script that generates AST information."""
        return """
const ts = require('typescript');
const fs = require('fs');

const fileName = process.argv[2];
const sourceCode = fs.readFileSync(fileName, 'utf-8');
const sourceFile = ts.createSourceFile(
    fileName,
    sourceCode,
    ts.ScriptTarget.Latest,
    true
);

function getNodePosition(node) {
    const { line, character } = sourceFile.getLineAndCharacterOfPosition(node.getStart());
    return {
        startLine: line + 1,
        startChar: character,
        endLine: sourceFile.getLineAndCharacterOfPosition(node.getEnd()).line + 1,
        endChar: sourceFile.getLineAndCharacterOfPosition(node.getEnd()).character
    };
}

function extractFunctions(node) {
    const functions = [];
    
    function visit(node) {
        if (ts.isFunctionDeclaration(node) || 
            ts.isMethodDeclaration(node) || 
            ts.isArrowFunction(node) ||
            ts.isFunctionExpression(node)) {
            
            const name = node.name ? node.name.getText() : 'anonymous';
            const pos = getNodePosition(node);
            const params = node.parameters.map(p => ({
                name: p.name.getText(),
                type: p.type ? p.type.getText() : 'any'
            }));
            
            functions.push({
                name,
                kind: node.kind,
                pos,
                params,
                isAsync: node.modifiers?.some(m => m.kind === ts.SyntaxKind.AsyncKeyword) || false,
                returnType: node.type ? node.type.getText() : 'any'
            });
        }
        
        ts.forEachChild(node, visit);
    }
    
    visit(sourceFile);
    return functions;
}

const functions = extractFunctions(sourceFile);
console.log(JSON.stringify(functions, null, 2));
"""

    @staticmethod
    def _extract_code_segment(file_content: str, start_line: int, end_line: int) -> str:
        """Extract a segment of code from the file content."""
        lines = file_content.split("\n")
        return "\n".join(lines[start_line - 1 : end_line])

    def parse_file(self, file_path: str) -> List[Tuple[str, str, dict]]:
        """
        Parse a TypeScript file and extract function information.

        Args:
            file_path (str): Path to the TypeScript file

        Returns:
            List[Tuple[str, str, dict]]: List of tuples containing
                (function_name, function_code, metadata)
        """
        # Create temporary directory for our parser script
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the parser script
            parser_path = os.path.join(temp_dir, "parser.js")
            with open(parser_path, "w") as f:
                f.write(self._create_ast_generator_script())

            # Read the original file content
            with open(file_path, "r") as f:
                file_content = f.read()

            # Run the parser script
            try:
                result = subprocess.run(
                    ["node", parser_path, file_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                functions_data = json.loads(result.stdout)
            except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
                raise Exception(f"Failed to parse TypeScript file: {str(e)}")

            # Extract function information
            functions = []
            for func in functions_data:
                code = self._extract_code_segment(
                    file_content, func["pos"]["startLine"], func["pos"]["endLine"]
                )

                metadata = {
                    "isAsync": func["isAsync"],
                    "parameters": func["params"],
                    "returnType": func["returnType"],
                }

                functions.append((func["name"], code, metadata))

            return functions
