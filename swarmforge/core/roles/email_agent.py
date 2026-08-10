"""email agent agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_email_agent_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "email-agent",
        role=AgentRole.WORKER,
        description="email agent specialist agent",
        capabilities=["email agent"],
        model=model,
        provider=provider,
    )
