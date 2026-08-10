"""Advanced example: error handling."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="error-handling", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate error handling")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
