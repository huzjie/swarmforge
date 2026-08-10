# Getting Started

## Installation
```bash
pip install -e .
```

## Quick Start
1. Copy `.env.example` to `.env`
2. Add your API keys
3. Run: `swarmforge serve start`

## First Agent
```python
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
agent = Agent(AgentConfig(name="hello", role=AgentRole.WORKER))
result = await agent.run("Say hello!")
```