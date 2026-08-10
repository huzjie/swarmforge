"""
Tests for the Swarm module.
"""
import pytest
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology
from swarmforge.core.agent import Agent, AgentConfig, AgentRole


class TestSwarmConfig:
    def test_default_config(self):
        config = SwarmConfig(name="test-swarm")
        assert config.name == "test-swarm"
        assert config.topology == SwarmTopology.PARALLEL
        assert config.max_concurrent_agents == 10

    def test_custom_topology(self):
        for topo in SwarmTopology:
            config = SwarmConfig(name="test", topology=topo)
            assert config.topology == topo


class TestSwarm:
    def test_swarm_creation(self, swarm_config):
        swarm = Swarm(swarm_config)
        assert swarm.config.name == "test-swarm"
        assert len(swarm.agents) == 0

    def test_add_agent(self, swarm_config):
        swarm = Swarm(swarm_config)
        cfg = AgentConfig(name="worker-1", role=AgentRole.WORKER, capabilities=["search"])
        agent = Agent(cfg)
        swarm.add_agent(agent)
        assert len(swarm.agents) == 1
        assert "worker-1" in swarm.agents

    def test_add_multiple_agents(self, swarm_config):
        swarm = Swarm(swarm_config)
        for i in range(5):
            cfg = AgentConfig(name=f"agent-{i}", role=AgentRole.WORKER, capabilities=[f"skill-{i}"])
            swarm.add_agent(Agent(cfg))
        assert len(swarm.agents) == 5

    def test_remove_agent(self, swarm):
        assert len(swarm.agents) == 3
        swarm.remove_agent("worker-0")
        assert len(swarm.agents) == 2
        assert "worker-0" not in swarm.agents

    def test_get_agent(self, swarm):
        agent = swarm.get_agent("worker-1")
        assert agent is not None
        assert agent.config.name == "worker-1"
        assert swarm.get_agent("nonexistent") is None

    @pytest.mark.asyncio
    async def test_swarm_run_parallel(self, swarm):
        run = await swarm.run("Test task")
        assert run.status == "completed"
        assert len(run.results) == 3
        assert run.topology == "parallel"

    @pytest.mark.asyncio
    async def test_swarm_run_sequential(self, swarm_config):
        swarm_config.topology = SwarmTopology.SEQUENTIAL
        swarm = Swarm(swarm_config)
        for i in range(2):
            cfg = AgentConfig(name=f"seq-{i}", role=AgentRole.WORKER)
            swarm.add_agent(Agent(cfg))
        run = await swarm.run("Sequential task")
        assert run.status == "completed"

    @pytest.mark.asyncio
    async def test_swarm_run_broadcast(self, swarm_config):
        swarm_config.topology = SwarmTopology.BROADCAST
        swarm = Swarm(swarm_config)
        for i in range(2):
            cfg = AgentConfig(name=f"bc-{i}", role=AgentRole.WORKER)
            swarm.add_agent(Agent(cfg))
        run = await swarm.run("Broadcast task")
        assert run.status == "completed"

    def test_swarm_stats(self, swarm):
        stats = swarm.get_stats()
        assert stats["name"] == "test-swarm"
        assert stats["agent_count"] == 3
        assert stats["topology"] == "parallel"

    @pytest.mark.asyncio
    async def test_empty_swarm_run(self, swarm_config):
        swarm = Swarm(swarm_config)
        run = await swarm.run("Task with no agents")
        assert run.status == "completed"
        assert len(run.results) == 0
