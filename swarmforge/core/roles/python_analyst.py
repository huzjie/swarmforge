"""python analyst agent role definition."""
from swarmforge.core.agent import AgentConfig, AgentRole

def create_python_analyst_agent(name: str = None, model: str = "gpt-4", provider: str = "openai"):
    return AgentConfig(
        name=name or "python-analyst",
        role=AgentRole.WORKER,
        description="python analyst specialist agent",
        capabilities=["python analyst"],
        model=model,
        provider=provider,
    )
