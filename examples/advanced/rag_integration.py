"""Advanced example: rag integration."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="rag-integration", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate rag integration")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
