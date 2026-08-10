"""Data processing tools for agents."""
from swarmforge.core.tool import Tool, ToolResult
import json

class DataAnalysisTool:
    @staticmethod
    async def analyze_json(data: str) -> ToolResult:
        try:
            parsed = json.loads(data)
            if isinstance(parsed, list):
                stats = {"count": len(parsed), "type": "list"}
            elif isinstance(parsed, dict):
                stats = {"keys": list(parsed.keys()), "type": "dict"}
            else:
                stats = {"type": type(parsed).__name__}
            return ToolResult(success=True, data=stats)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    @staticmethod
    async def summarize_text(text: str, max_length: int = 200) -> ToolResult:
        if len(text) <= max_length:
            return ToolResult(success=True, data={"summary": text, "truncated": False})
        sentences = text.replace("!", ".").replace("?", ".").split(".")
        summary = ""
        for s in sentences:
            if len(summary) + len(s) <= max_length:
                summary += s + "."
            else:
                break
        return ToolResult(success=True, data={"summary": summary.strip(), "truncated": True, "original_length": len(text)})
