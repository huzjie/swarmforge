"""
SwarmForge Tool System — type-safe tool definitions with validation.
"""
from __future__ import annotations

import inspect
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, get_type_hints


@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
        }


class Tool:
    """A tool that an agent can call."""

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Optional[List[ToolParameter]] = None,
        require_confirmation: bool = False,
        timeout_seconds: int = 60,
    ):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or self._infer_parameters(func)
        self.require_confirmation = require_confirmation
        self.timeout_seconds = timeout_seconds

    def _infer_parameters(self, func: Callable) -> List[ToolParameter]:
        """Infer parameters from function signature and type hints."""
        params = []
        sig = inspect.signature(func)
        hints = get_type_hints(func) if hasattr(func, "__annotations__") else {}

        for pname, param in sig.parameters.items():
            if pname == "self":
                continue
            param_type = hints.get(pname, "string")
            type_str = getattr(param_type, "__name__", str(param_type))
            has_default = param.default is not inspect.Parameter.empty
            params.append(ToolParameter(
                name=pname,
                type=type_str,
                description=f"Parameter: {pname}",
                required=not has_default,
                default=param.default if has_default else None,
            ))
        return params

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function-calling schema."""
        properties = {}
        required = []
        for p in self.parameters:
            type_map = {"str": "string", "int": "integer", "float": "number", "bool": "boolean"}
            properties[p.name] = {
                "type": type_map.get(p.type, "string"),
                "description": p.description,
            }
            if p.required:
                required.append(p.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with the given arguments."""
        try:
            result = self.func(**kwargs)
            if inspect.isawaitable(result):
                result = await result
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def __call__(self, **kwargs):
        return self.func(**kwargs)


class ToolRegistry:
    """Registry for managing and discovering tools."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list(self) -> List[Tool]:
        return list(self._tools.values())

    def get_openai_schemas(self) -> List[Dict[str, Any]]:
        return [t.to_openai_schema() for t in self._tools.values()]

    def get_anthropic_schemas(self) -> List[Dict[str, Any]]:
        schemas = []
        for t in self._tools.values():
            schemas.append({
                "name": t.name,
                "description": t.description,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        p.name: {"type": p.type, "description": p.description}
                        for p in t.parameters
                    },
                    "required": [p.name for p in t.parameters if p.required],
                },
            })
        return schemas


# --- Built-in Tools ---
registry = ToolRegistry()

@Tool("web_search", "Search the web for information", lambda query: {"results": [f"Search result for: {query}"]})
def _search_tool():
    pass

@Tool("read_file", "Read contents of a file", lambda path: {"content": f"Contents of {path}"})
def _read_file_tool():
    pass

@Tool("write_file", "Write content to a file", lambda path, content: {"written": path})
def _write_file_tool():
    pass

@Tool("execute_python", "Execute Python code in sandbox", lambda code: {"output": f"Executed: {code[:50]}..."})
def _execute_python_tool():
    pass

@Tool("send_message", "Send a message to another agent or user", lambda to, message: {"sent": True, "to": to})
def _send_message_tool():
    pass
