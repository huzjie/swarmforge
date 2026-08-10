"""Advanced example: prompt chaining."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="prompt-chaining", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate prompt chaining")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
