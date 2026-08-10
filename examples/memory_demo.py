"""Example: Using persistent memory across agent runs."""
import asyncio
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.memory import MemoryEntry, MemoryType

async def main():
    agent = Agent(AgentConfig(name="memory-bot", role=AgentRole.WORKER, system_prompt="Remember user preferences and use them."))

    # Store a preference
    agent.long_term_memory.add(MemoryEntry(id="pref-1", content="User prefers Python over JavaScript", memory_type=MemoryType.LONG_TERM, importance=0.9))

    # Later, retrieve it
    results = agent.long_term_memory.search("Python preference")
    for r in results:
        print(f"Memory: {r.content} (importance: {r.importance})")

    result = await agent.run("What programming language should I use for this task?")
    print(f"Agent response: {result['response']}")

if __name__ == "__main__":
    asyncio.run(main())
