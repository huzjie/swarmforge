"""Advanced example: streaming agent."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="streaming-agent", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate streaming agent")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
