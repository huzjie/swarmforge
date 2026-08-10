"""
Example: Switching between LLM providers.
"""
import asyncio
from swarmforge.providers.provider_registry import get_provider


async def main():
    messages = [{"role": "user", "content": "Say hello in 3 languages"}]

    # Try different providers
    for provider_name in ["openai", "deepseek"]:
        try:
            provider = get_provider(provider_name)
            print(f"\n=== {provider.provider_name} ===")
            response = await provider.chat(messages, model="gpt-4" if provider_name == "openai" else "deepseek-chat")
            print(f"Response: {response.content[:200]}")
            print(f"Tokens: {response.usage}")
        except Exception as e:
            print(f"Provider {provider_name} not available: {e}")


if __name__ == "__main__":
    asyncio.run(main())
