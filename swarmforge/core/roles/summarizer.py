"""summarizer agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_summarizer_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "summarizer",
        role=AgentRole.WORKER,
        description="summarizer specialist agent",
        capabilities=["summarizer"],
        model=model,
        provider=provider,
    )
