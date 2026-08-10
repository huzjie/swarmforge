"""
Tests for the Tool system.
"""
import pytest
from swarmforge.core.tool import Tool, ToolRegistry, ToolResult


class TestTool:
    def test_tool_creation(self):
        def my_func(x: int, y: str = "default") -> str:
            return f"{x}: {y}"

        tool = Tool(name="my_tool", description="Test tool", func=my_func)
        assert tool.name == "my_tool"
        assert tool.description == "Test tool"
        assert len(tool.parameters) == 2

    def test_tool_openai_schema(self):
        def search(query: str) -> dict:
            return {"results": []}

        tool = Tool(name="search", description="Search the web", func=search)
        schema = tool.to_openai_schema()
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "search"
        assert "query" in schema["function"]["parameters"]["properties"]

    def test_tool_execute_sync(self):
        def add(a: int, b: int) -> int:
            return a + b

        tool = Tool(name="add", description="Add numbers", func=add)
        result = tool(a=1, b=2)
        assert result == 3


class TestToolRegistry:
    def test_register_and_get(self):
        reg = ToolRegistry()
        tool = Tool(name="test", description="test", func=lambda: "ok")
        reg.register(tool)
        assert reg.get("test") is not None
        assert reg.get("nonexistent") is None

    def test_list_tools(self):
        reg = ToolRegistry()
        reg.register(Tool(name="t1", description="d1", func=lambda: 1))
        reg.register(Tool(name="t2", description="d2", func=lambda: 2))
        assert len(reg.list()) == 2

    def test_openai_schemas(self):
        reg = ToolRegistry()
        reg.register(Tool(name="search", description="Search", func=lambda q: None))
        schemas = reg.get_openai_schemas()
        assert len(schemas) == 1
        assert schemas[0]["function"]["name"] == "search"
