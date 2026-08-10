"""
Example: Parallel swarm execution.
"""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology


async def main():
    swarm = Swarm(SwarmConfig(
        name="research-team",
        topology=SwarmTopology.PARALLEL,
    ))

    # Add specialized agents
    agents = [
        ("market-researcher", AgentRole.RESEARCHER, ["market_analysis"]),
        ("data-analyst", AgentRole.ANALYST, ["data_processing"]),
        ("content-writer", AgentRole.WORKER, ["content_creation"]),
    ]

    for name, role, caps in agents:
        config = AgentConfig(name=name, role=role, capabilities=caps)
        swarm.add_agent(Agent(config))

    result = await swarm.run("Research the AI agent market and create a report")
    print(f"Swarm status: {result.status}")
    for i, r in enumerate(result.results):
        print(f"  Agent {i+1}: {r['agent_name']} - {r['success']}")


if __name__ == "__main__":
    asyncio.run(main())
