"""Advanced example: load balancing."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="load-balancing", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate load balancing")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
