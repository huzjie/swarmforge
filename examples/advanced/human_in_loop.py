"""Advanced example: human in loop."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole

async def main():
    agent = Agent(AgentConfig(name="human-in-loop", role=AgentRole.WORKER))
    result = await agent.run("Demonstrate human in loop")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
