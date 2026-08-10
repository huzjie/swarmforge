"""
Pytest fixtures for SwarmForge tests.
"""
import pytest
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology
from swarmforge.core.tool import ToolRegistry, Tool


@pytest.fixture
def tool_registry():
    reg = ToolRegistry()
    return reg


@pytest.fixture
def agent_config():
    return AgentConfig(
        name="test-agent",
        role=AgentRole.WORKER,
        description="Test agent",
        model="gpt-4",
        provider="openai",
        capabilities=["test", "analysis"],
        tools=["web_search"],
    )


@pytest.fixture
def agent(agent_config, tool_registry):
    return Agent(agent_config, tool_registry)


@pytest.fixture
def swarm_config():
    return SwarmConfig(
        name="test-swarm",
        topology=SwarmTopology.PARALLEL,
        max_concurrent_agents=5,
    )


@pytest.fixture
def swarm(swarm_config):
    s = Swarm(swarm_config)
    for i in range(3):
        cfg = AgentConfig(
            name=f"worker-{i}",
            role=AgentRole.WORKER,
            capabilities=[f"skill-{i}"],
        )
        s.add_agent(Agent(cfg))
    return s
