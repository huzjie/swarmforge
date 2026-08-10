"""
Anthropic provider — Claude models.
"""
from __future__ import annotations

from typing import Any, AsyncIterator, Dict, List, Optional

from swarmforge.providers.base import BaseProvider, LLMResponse


class AnthropicProvider(BaseProvider):
    """Provider for Anthropic Claude API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def _get_client(self):
        try:
            from anthropic import AsyncAnthropic
            return AsyncAnthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package required: pip install anthropic")

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "claude-sonnet-4-20250514",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None,
        **kwargs,
    ) -> LLMResponse:
        client = self._get_client()

        # Extract system message
        system_msg = ""
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                user_messages.append(m)

        params = {
            "model": model,
            "messages": user_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_msg:
            params["system"] = system_msg
        if tools:
            params["tools"] = tools

        response = await client.messages.create(**params, **kwargs)

        tool_calls = None
        content_blocks = []
        for block in response.content:
            if block.type == "text":
                content_blocks.append(block.text)
            elif block.type == "tool_use":
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append({
                    "id": block.id,
                    "function": {"name": block.name, "arguments": str(block.input)},
                })

        return LLMResponse(
            content="
".join(content_blocks),
            model=response.model,
            finish_reason=response.stop_reason or "stop",
            usage={
                "input_tokens": response.usage.input_tokens if response.usage else 0,
                "output_tokens": response.usage.output_tokens if response.usage else 0,
            },
            tool_calls=tool_calls,
        )

    async def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str = "claude-sonnet-4-20250514",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> AsyncIterator[str]:
        client = self._get_client()
        system_msg = ""
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                user_messages.append(m)

        async with client.messages.stream(
            model=model,
            messages=user_messages,
            system=system_msg,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def list_models(self) -> List[str]:
        return ["claude-opus-4-20250514", "claude-sonnet-4-20250514", "claude-haiku-3.5"]
