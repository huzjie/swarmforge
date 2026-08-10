"""triage agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_triage_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "triage",
        role=AgentRole.WORKER,
        description="triage specialist agent",
        capabilities=["triage"],
        model=model,
        provider=provider,
    )
