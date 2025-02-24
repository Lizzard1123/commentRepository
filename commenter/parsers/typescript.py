import os
from typing import List, Tuple
import subprocess
import json
import tempfile


class TypeScriptParser:
    """Parser for TypeScript files to extract function, class, type, and interface information."""

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

function extractElements(node) {
    const elements = [];
    
    function visit(node) {
        let element = null;
        
        // Handle variable declarations with arrow functions, function expressions
        if (ts.isVariableStatement(node)) {
            node.declarationList.declarations.forEach(declaration => {
                if (declaration.initializer && 
                    (ts.isArrowFunction(declaration.initializer) || ts.isFunctionExpression(declaration.initializer))) {
                    const name = declaration.name.getText();
                    const pos = getNodePosition(node);
                    const params = declaration.initializer.parameters.map(p => ({
                        name: p.name.getText(),
                        type: p.type ? p.type.getText() : 'any'
                    }));
                    
                    element = {
                        type: 'function',
                        name,
                        pos,
                        params,
                        isAsync: declaration.initializer.modifiers?.some(m => m.kind === ts.SyntaxKind.AsyncKeyword) || false,
                        returnType: declaration.initializer.type ? declaration.initializer.type.getText() : 'any'
                    };
                    
                    elements.push(element);
                }
            });
            
            // Continue to check child nodes
            ts.forEachChild(node, visit);
            return;
        }
        
        if (ts.isFunctionDeclaration(node) || ts.isMethodDeclaration(node)) {
            const name = node.name ? node.name.getText() : 'anonymous';
            const pos = getNodePosition(node);
            const params = node.parameters.map(p => ({
                name: p.name.getText(),
                type: p.type ? p.type.getText() : 'any'
            }));
            
            element = {
                type: 'function',
                name,
                pos,
                params,
                isAsync: node.modifiers?.some(m => m.kind === ts.SyntaxKind.AsyncKeyword) || false,
                returnType: node.type ? node.type.getText() : 'any'
            };
        } else if (ts.isClassDeclaration(node) && node.name) {
            element = {
                type: 'class',
                name: node.name.getText(),
                pos: getNodePosition(node)
            };
        } else if (ts.isTypeAliasDeclaration(node)) {
            element = {
                type: 'type',
                name: node.name.getText(),
                pos: getNodePosition(node)
            };
        } else if (ts.isInterfaceDeclaration(node)) {
            element = {
                type: 'interface',
                name: node.name.getText(),
                pos: getNodePosition(node)
            };
        }
        
        if (element) {
            elements.push(element);
        }
        
        ts.forEachChild(node, visit);
    }
    
    visit(sourceFile);
    return elements;
}

const elements = extractElements(sourceFile);
console.log(JSON.stringify(elements, null, 2));
"""

    @staticmethod
    def _extract_code_segment(file_content: str, start_line: int, end_line: int) -> str:
        """Extract a segment of code from the file content."""
        lines = file_content.split("\n")
        return "\n".join(lines[start_line - 1 : end_line])

    def parse_file(self, file_path: str) -> List[Tuple[str, str, dict]]:
        """
        Parse a TypeScript file and extract function, class, type, and interface information.

        Args:
            file_path (str): Path to the TypeScript file

        Returns:
            List[Tuple[str, str, dict]]: List of tuples containing
                (element_name, element_code, metadata)
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            parser_path = os.path.join(temp_dir, "parser.js")
            with open(parser_path, "w") as f:
                f.write(self._create_ast_generator_script())

            with open(file_path, "r") as f:
                file_content = f.read()

            try:
                result = subprocess.run(
                    ["node", parser_path, file_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                elements_data = json.loads(result.stdout)
            except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
                raise Exception(f"Failed to parse TypeScript file: {str(e)}")

            elements = []
            for elem in elements_data:
                code = self._extract_code_segment(
                    file_content, elem["pos"]["startLine"], elem["pos"]["endLine"]
                )
                metadata = {k: v for k, v in elem.items()}
                elements.append((elem["name"], code, metadata))

            return elements
