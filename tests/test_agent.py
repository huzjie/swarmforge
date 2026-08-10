"""
Tests for the Agent module.
"""
import pytest
from swarmforge.core.agent import Agent, AgentConfig, AgentRole


class TestAgentConfig:
    def test_default_config(self):
        config = AgentConfig(name="test", role=AgentRole.WORKER)
        assert config.name == "test"
        assert config.role == AgentRole.WORKER
        assert config.model == "gpt-4"
        assert config.provider == "openai"
        assert config.temperature == 0.7
        assert config.max_iterations == 10

    def test_custom_config(self):
        config = AgentConfig(
            name="custom",
            role=AgentRole.ORCHESTRATOR,
            model="claude-opus-4-20250514",
            provider="anthropic",
            temperature=0.3,
            max_tokens=8192,
            capabilities=["planning", "delegation"],
            max_iterations=20,
        )
        assert config.name == "custom"
        assert config.role == AgentRole.ORCHESTRATOR
        assert config.provider == "anthropic"
        assert config.temperature == 0.3


class TestAgent:
    def test_agent_creation(self, agent_config):
        agent = Agent(agent_config)
        assert agent.config.name == "test-agent"
        assert agent.id is not None
        assert len(agent.id) == 8

    def test_agent_system_prompt(self, agent_config):
        agent = Agent(agent_config)
        msgs = agent.memory.get_messages()
        assert len(msgs) > 0
        assert msgs[0]["role"] == "system"

    def test_agent_custom_prompt(self):
        config = AgentConfig(
            name="custom-prompt",
            role=AgentRole.WORKER,
            system_prompt="You are a specialized code reviewer.",
        )
        agent = Agent(config)
        msgs = agent.memory.get_messages()
        assert "code reviewer" in msgs[0]["content"]

    @pytest.mark.asyncio
    async def test_agent_run(self, agent):
        result = await agent.run("Hello, world!")
        assert result["success"] is True
        assert result["agent_name"] == "test-agent"
        assert "response" in result
        assert "latency_ms" in result

    @pytest.mark.asyncio
    async def test_agent_run_with_context(self, agent):
        result = await agent.run("Analyze data", {"dataset": "sales_2026"})
        assert result["success"] is True

    def test_agent_handoff(self, agent):
        ctx = agent.handoff("other-agent", "Please review this")
        assert ctx.source_agent == "test-agent"
        assert ctx.target_agent == "other-agent"
        assert ctx.message == "Please review this"

    def test_agent_stats(self, agent):
        stats = agent.get_stats()
        assert stats["name"] == "test-agent"
        assert stats["role"] == "worker"
        assert "total_tokens" in stats
        assert "total_latency_ms" in stats
