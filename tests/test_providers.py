"""Tests for LLM providers."""
import pytest
from swarmforge.providers.openai_provider import OpenAIProvider
from swarmforge.providers.anthropic_provider import AnthropicProvider
from swarmforge.providers.deepseek_provider import DeepSeekProvider
from swarmforge.providers.google_provider import GoogleProvider
from swarmforge.providers.provider_registry import ProviderRegistry

class TestProviderRegistry:
    def test_list_providers(self):
        providers = ProviderRegistry.list_providers()
        assert "openai" in providers
        assert "anthropic" in providers
        assert "deepseek" in providers
        assert "google" in providers

    def test_get_default_provider(self):
        provider = ProviderRegistry.get("openai")
        assert provider.provider_name == "openai"

    def test_get_unknown_provider(self):
        with pytest.raises(ValueError):
            ProviderRegistry.get("unknown-provider")
