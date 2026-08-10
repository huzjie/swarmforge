"""fact checker agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_fact_checker_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "fact-checker",
        role=AgentRole.WORKER,
        description="fact checker specialist agent",
        capabilities=["fact checker"],
        model=model,
        provider=provider,
    )
