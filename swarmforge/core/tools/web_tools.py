"""Web-related tools for agents."""
from swarmforge.core.tool import Tool, ToolResult
import json

class WebSearchTool:
    @staticmethod
    async def search(query: str, num_results: int = 5) -> ToolResult:
        return ToolResult(success=True, data={"query": query, "results": [f"Result {i+1} for: {query}" for i in range(num_results)]})

class URLFetcherTool:
    @staticmethod
    async def fetch(url: str) -> ToolResult:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(url)
                return ToolResult(success=True, data={"url": url, "status": resp.status_code, "content_preview": resp.text[:2000]})
        except Exception as e:
            return ToolResult(success=False, error=str(e))
