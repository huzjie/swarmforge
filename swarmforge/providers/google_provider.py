"""
Google provider — Gemini models.
"""
from __future__ import annotations

from typing import Any, AsyncIterator, Dict, List, Optional

from swarmforge.providers.base import BaseProvider, LLMResponse


class GoogleProvider(BaseProvider):
    """Provider for Google Gemini API."""

    @property
    def provider_name(self) -> str:
        return "google"

    async def chat(self, messages, model="gemini-2.0-flash", temperature=0.7, max_tokens=4096, tools=None, **kwargs):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            mdl = genai.GenerativeModel(model)
            prompt = self._convert_messages(messages)
            response = await mdl.generate_content_async(prompt)
            return LLMResponse(
                content=response.text,
                model=model,
                finish_reason="stop",
            )
        except ImportError:
            raise ImportError("google-generativeai package required: pip install google-generativeai")

    async def chat_stream(self, messages, model="gemini-2.0-flash", temperature=0.7, max_tokens=4096, **kwargs):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            mdl = genai.GenerativeModel(model)
            prompt = self._convert_messages(messages)
            response = await mdl.generate_content_async(prompt, stream=True)
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except ImportError:
            raise ImportError("google-generativeai package required")

    def _convert_messages(self, messages: List[Dict]) -> str:
        parts = []
        for m in messages:
            parts.append(f"[{m['role']}]: {m['content']}")
        return "\n".join(parts)

    async def list_models(self) -> List[str]:
        return ["gemini-2.0-flash", "gemini-2.0-pro", "gemini-2.5-pro"]
