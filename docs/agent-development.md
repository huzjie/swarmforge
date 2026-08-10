# Agent Development

## Creating Custom Agents
```python
config = AgentConfig(
    name="my-agent",
    role=AgentRole.CUSTOM,
    system_prompt="You are a specialized agent...",
    capabilities=["my-skill"],
    tools=["web_search", "execute_python"],
)
agent = Agent(config)
```

## Agent Lifecycle
1. Receive task
2. Think (LLM call)
3. Act (tool execution)
4. Observe (process result)
5. Repeat until done or max iterations