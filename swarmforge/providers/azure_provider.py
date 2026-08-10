"""Azure OpenAI provider."""
from swarmforge.providers.base import BaseProvider, LLMResponse
from typing import List, Dict, Any, Optional, AsyncIterator

class AzureProvider(BaseProvider):
    @property
    def provider_name(self): return "azure"
    def _get_client(self):
        from openai import AsyncAzureOpenAI
        return AsyncAzureOpenAI(api_key=self.api_key, azure_endpoint=self.base_url, api_version="2024-02-15-preview")
    async def chat(self, messages, model="gpt-4", temperature=0.7, max_tokens=4096, tools=None, **kwargs):
        client = self._get_client()
        params = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        if tools: params["tools"] = tools
        resp = await client.chat.completions.create(**params, **kwargs)
        c = resp.choices[0]
        return LLMResponse(content=c.message.content or "", model=resp.model, finish_reason=c.finish_reason or "stop")
    async def chat_stream(self, messages, model="gpt-4", temperature=0.7, max_tokens=4096, **kwargs):
        client = self._get_client()
        stream = await client.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, stream=True, **kwargs)
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    async def list_models(self): return ["gpt-4", "gpt-4o", "gpt-35-turbo"]
