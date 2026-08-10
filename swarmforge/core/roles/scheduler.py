"""scheduler agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_scheduler_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "scheduler",
        role=AgentRole.WORKER,
        description="scheduler specialist agent",
        capabilities=["scheduler"],
        model=model,
        provider=provider,
    )
