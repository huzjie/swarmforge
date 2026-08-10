"""Example: Hierarchical swarm execution."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology

async def main():
    swarm = Swarm(SwarmConfig(name="manager-team", topology=SwarmTopology.HIERARCHICAL))
    swarm.add_agent(Agent(AgentConfig(name="manager", role=AgentRole.ORCHESTRATOR, capabilities=["planning", "delegation"])))
    swarm.add_agent(Agent(AgentConfig(name="researcher-1", role=AgentRole.RESEARCHER, capabilities=["web_search"])))
    swarm.add_agent(Agent(AgentConfig(name="analyst-1", role=AgentRole.ANALYST, capabilities=["data_analysis"])))
    result = await swarm.run("Research the AI agent market in 2026 and provide analysis")
    print(f"Status: {result.status}")
    for r in result.results:
        print(f"  {r.get('agent_name', 'unknown')}: {'OK' if r.get('success') else 'FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
