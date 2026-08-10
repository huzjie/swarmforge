"""sentiment agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_sentiment_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "sentiment",
        role=AgentRole.WORKER,
        description="sentiment specialist agent",
        capabilities=["sentiment"],
        model=model,
        provider=provider,
    )
