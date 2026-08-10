"""Ai21 provider adapter for SwarmForge."""
from swarmforge.providers.base import BaseProvider, LLMResponse
from typing import List, Dict, Any, Optional, AsyncIterator

class Ai21Adapter(BaseProvider):
    @property
    def provider_name(self): return "ai21"
    async def chat(self, messages, model="default", temperature=0.7, max_tokens=4096, tools=None, **kwargs):
        return LLMResponse(content="[Ai21 response]", model=model)
    async def chat_stream(self, messages, model="default", temperature=0.7, max_tokens=4096, **kwargs):
        yield "[Ai21 stream]"
    async def list_models(self): return ["default"]
