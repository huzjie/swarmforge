"""
Provider registry — manage and switch between LLM providers.
"""
from __future__ import annotations

from typing import Dict, Optional, Type

from swarmforge.config import settings
from swarmforge.providers.base import BaseProvider
from swarmforge.providers.openai_provider import OpenAIProvider
from swarmforge.providers.anthropic_provider import AnthropicProvider
from swarmforge.providers.deepseek_provider import DeepSeekProvider
from swarmforge.providers.google_provider import GoogleProvider


class ProviderRegistry:
    """Central registry for LLM providers."""

    _providers: Dict[str, Type[BaseProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "deepseek": DeepSeekProvider,
        "google": GoogleProvider,
    }

    _instances: Dict[str, BaseProvider] = {}

    @classmethod
    def register(cls, name: str, provider_cls: Type[BaseProvider]) -> None:
        cls._providers[name] = provider_cls

    @classmethod
    def get(cls, name: Optional[str] = None) -> BaseProvider:
        name = name or settings.llm_default_provider
        if name not in cls._instances:
            provider_cls = cls._providers.get(name)
            if not provider_cls:
                raise ValueError(f"Unknown provider: {name}. Available: {list(cls._providers.keys())}")

            kwargs = {}
            if name == "openai":
                kwargs["api_key"] = settings.openai_api_key
                kwargs["base_url"] = settings.openai_base_url
            elif name == "anthropic":
                kwargs["api_key"] = settings.anthropic_api_key
            elif name == "deepseek":
                kwargs["api_key"] = settings.deepseek_api_key
                kwargs["base_url"] = settings.deepseek_base_url
            elif name == "google":
                kwargs["api_key"] = settings.google_api_key

            cls._instances[name] = provider_cls(**kwargs)

        return cls._instances[name]

    @classmethod
    def list_providers(cls) -> Dict[str, Type[BaseProvider]]:
        return dict(cls._providers)

    @classmethod
    def reset(cls) -> None:
        cls._instances.clear()


def get_provider(name: Optional[str] = None) -> BaseProvider:
    return ProviderRegistry.get(name)
