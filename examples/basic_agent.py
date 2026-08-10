"""
Example: Basic agent usage.
"""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole


async def main():
    config = AgentConfig(
        name="assistant",
        role=AgentRole.WORKER,
        description="A helpful AI assistant",
        system_prompt="You are a helpful assistant. Answer questions concisely.",
    )
    agent = Agent(config)

    result = await agent.run("What is the capital of France?")
    print(f"Response: {result['response']}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
    print(f"Iterations: {result['iterations']}")


if __name__ == "__main__":
    asyncio.run(main())
