"""Groq provider — ultra-fast inference."""
from swarmforge.providers.base import BaseProvider, LLMResponse
from typing import List, Dict, Any, Optional, AsyncIterator

class GroqProvider(BaseProvider):
    @property
    def provider_name(self): return "groq"
    def _get_client(self):
        from openai import AsyncOpenAI
        return AsyncOpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
    async def chat(self, messages, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=4096, tools=None, **kwargs):
        client = self._get_client()
        params = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        resp = await client.chat.completions.create(**params, **kwargs)
        c = resp.choices[0]
        return LLMResponse(content=c.message.content or "", model=resp.model, finish_reason=c.finish_reason or "stop")
    async def chat_stream(self, messages, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=4096, **kwargs):
        client = self._get_client()
        stream = await client.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, stream=True, **kwargs)
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    async def list_models(self): return ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
