"""Advanced example: evaluation pipeline."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="evaluation-pipeline", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate evaluation pipeline")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
