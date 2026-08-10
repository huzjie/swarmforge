"""translator agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_translator_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "translator",
        role=AgentRole.WORKER,
        description="translator specialist agent",
        capabilities=["translator"],
        model=model,
        provider=provider,
    )
