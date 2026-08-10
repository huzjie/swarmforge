"""
Example: Sequential swarm execution (pipeline).
"""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology


async def main():
    swarm = Swarm(SwarmConfig(
        name="code-review-pipeline",
        topology=SwarmTopology.SEQUENTIAL,
    ))

    # Code generation → review → test pipeline
    swarm.add_agent(Agent(AgentConfig(
        name="code-generator", role=AgentRole.CODER,
        capabilities=["code_generation"],
    )))
    swarm.add_agent(Agent(AgentConfig(
        name="code-reviewer", role=AgentRole.REVIEWER,
        capabilities=["code_review", "security_audit"],
    )))
    swarm.add_agent(Agent(AgentConfig(
        name="test-writer", role=AgentRole.WORKER,
        capabilities=["test_generation"],
    )))

    result = await swarm.run("Write a Python function to validate email addresses")
    print(f"Pipeline status: {result.status}")
    for i, r in enumerate(result.results):
        print(f"  Step {i+1}: {r['agent_name']}")


if __name__ == "__main__":
    asyncio.run(main())
