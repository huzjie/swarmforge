"""File system tools for agents."""
from swarmforge.core.tool import Tool, ToolResult
from pathlib import Path
import json

class FileTools:
    @staticmethod
    async def read(path: str) -> ToolResult:
        try:
            content = Path(path).read_text(encoding="utf-8")
            return ToolResult(success=True, data={"path": path, "content": content, "size": len(content)})
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    @staticmethod
    async def write(path: str, content: str) -> ToolResult:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(content, encoding="utf-8")
            return ToolResult(success=True, data={"path": path, "written": True})
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    @staticmethod
    async def list_dir(path: str = ".") -> ToolResult:
        try:
            entries = []
            for p in Path(path).iterdir():
                entries.append({"name": p.name, "type": "dir" if p.is_dir() else "file", "size": p.stat().st_size if p.is_file() else 0})
            return ToolResult(success=True, data={"path": path, "entries": entries, "count": len(entries)})
        except Exception as e:
            return ToolResult(success=False, error=str(e))
