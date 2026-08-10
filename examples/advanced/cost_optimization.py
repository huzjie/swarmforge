"""Advanced example: cost optimization."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="cost-optimization", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate cost optimization")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
