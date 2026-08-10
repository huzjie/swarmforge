"""compliance agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_compliance_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "compliance",
        role=AgentRole.WORKER,
        description="compliance specialist agent",
        capabilities=["compliance"],
        model=model,
        provider=provider,
    )
