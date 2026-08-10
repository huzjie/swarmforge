"""notification agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_notification_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "notification",
        role=AgentRole.WORKER,
        description="notification specialist agent",
        capabilities=["notification"],
        model=model,
        provider=provider,
    )
