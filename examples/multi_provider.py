"""Example: Using multiple LLM providers in one swarm."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology

async def main():
    swarm = Swarm(SwarmConfig(name="multi-provider-team", topology=SwarmTopology.PARALLEL))
    swarm.add_agent(Agent(AgentConfig(name="gpt-agent", role=AgentRole.WORKER, model="gpt-4", provider="openai")))
    swarm.add_agent(Agent(AgentConfig(name="claude-agent", role=AgentRole.REVIEWER, model="claude-sonnet-4-20250514", provider="anthropic")))
    swarm.add_agent(Agent(AgentConfig(name="deepseek-agent", role=AgentRole.RESEARCHER, model="deepseek-chat", provider="deepseek")))
    result = await swarm.run("Compare cloud providers: AWS vs Azure vs GCP")
    print(f"Swarm: {result.status}, agents: {len(result.results)}")

if __name__ == "__main__":
    asyncio.run(main())
