"""Example: Creating and using custom tools."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.tool import Tool, ToolRegistry, ToolResult

async def main():
    registry = ToolRegistry()

    def get_weather(city: str) -> dict:
        return {"city": city, "temperature": 22, "condition": "sunny"}

    def calculate(expression: str) -> float:
        return eval(expression)

    registry.register(Tool(name="get_weather", description="Get weather for a city", func=get_weather))
    registry.register(Tool(name="calculate", description="Evaluate a math expression", func=calculate))

    agent = Agent(AgentConfig(
        name="weather-bot",
        role=AgentRole.WORKER,
        system_prompt="You are a helpful assistant. Use tools when needed.",
        tools=["get_weather", "calculate"],
    ), tool_registry=registry)

    result = await agent.run("What's the weather in Beijing?")
    print(f"Response: {result['response']}")

if __name__ == "__main__":
    asyncio.run(main())
