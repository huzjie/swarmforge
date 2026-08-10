"""Code-related tools for agents."""
from swarmforge.core.tool import Tool, ToolResult
from swarmforge.security.sandbox import Sandbox

sandbox = Sandbox()

class CodeExecutionTool:
    @staticmethod
    async def execute_python(code: str) -> ToolResult:
        result = sandbox.execute_python(code)
        return ToolResult(success=result["success"], data=result)

    @staticmethod
    async def execute_shell(command: str) -> ToolResult:
        result = sandbox.execute_shell(command)
        return ToolResult(success=result["success"], data=result)

class CodeAnalysisTool:
    @staticmethod
    async def analyze(file_path: str) -> ToolResult:
        try:
            import ast
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            return ToolResult(success=True, data={"file": file_path, "functions": functions, "classes": classes})
        except Exception as e:
            return ToolResult(success=False, error=str(e))
