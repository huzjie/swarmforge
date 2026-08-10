"""sql agent agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_sql_agent_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "sql-agent",
        role=AgentRole.WORKER,
        description="sql agent specialist agent",
        capabilities=["sql agent"],
        model=model,
        provider=provider,
    )
