"""Replicate provider adapter for SwarmForge."""
from swarmforge.providers.base import BaseProvider, LLMResponse
from typing import List, Dict, Any, Optional, AsyncIterator

class ReplicateAdapter(BaseProvider):
    @property
    def provider_name(self): return "replicate"
    async def chat(self, messages, model="default", temperature=0.7, max_tokens=4096, tools=None, **kwargs):
        return LLMResponse(content="[Replicate response]", model=model)
    async def chat_stream(self, messages, model="default", temperature=0.7, max_tokens=4096, **kwargs):
        yield "[Replicate stream]"
    async def list_models(self): return ["default"]
