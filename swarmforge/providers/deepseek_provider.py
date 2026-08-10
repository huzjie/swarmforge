"""
DeepSeek provider — DeepSeek-V3, DeepSeek-R1, DeepSeek-V4 models.
"""
from __future__ import annotations

from typing import Any, AsyncIterator, Dict, List, Optional

from swarmforge.providers.base import BaseProvider, LLMResponse


class DeepSeekProvider(BaseProvider):
    """Provider for DeepSeek API (OpenAI-compatible)."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url or "https://api.deepseek.com/v1")

    @property
    def provider_name(self) -> str:
        return "deepseek"

    def _get_client(self):
        try:
            from openai import AsyncOpenAI
            return AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            raise ImportError("openai package required: pip install openai")

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None,
        **kwargs,
    ) -> LLMResponse:
        client = self._get_client()
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            params["tools"] = tools

        response = await client.chat.completions.create(**params, **kwargs)
        choice = response.choices[0]

        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            finish_reason=choice.finish_reason or "stop",
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            },
        )

    async def chat_stream(self, messages, model="deepseek-chat", temperature=0.7, max_tokens=4096, **kwargs):
        client = self._get_client()
        stream = await client.chat.completions.create(
            model=model, messages=messages, temperature=temperature,
            max_tokens=max_tokens, stream=True, **kwargs,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def list_models(self) -> List[str]:
        return ["deepseek-chat", "deepseek-reasoner"]
