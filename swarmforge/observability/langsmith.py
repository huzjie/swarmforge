"""Langsmith observability integration."""
from typing import Dict, Any, Optional

class LangsmithTracer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def log_llm_call(self, model: str, prompt: str, response: str, metadata: Dict = None):
        pass

    def log_tool_call(self, tool: str, args: Dict, result: Any):
        pass

    def flush(self):
        pass
