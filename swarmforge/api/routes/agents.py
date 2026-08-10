"""
Agent management API endpoints.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from swarmforge.api.deps import verify_api_key, get_pagination
from swarmforge.core.agent import Agent, AgentConfig, AgentRole


router = APIRouter()

# In-memory store (replace with DB in production)
_agents: Dict[str, Agent] = {}


class AgentCreateRequest(BaseModel):
    name: str = Field(..., description="Agent name")
    role: str = Field("worker", description="Agent role")
    description: str = Field("", description="Agent description")
    system_prompt: str = Field("", description="Custom system prompt")
    model: str = Field("gpt-4", description="LLM model")
    provider: str = Field("openai", description="LLM provider")
    temperature: float = Field(0.7, ge=0, le=2.0)
    max_tokens: int = Field(4096, ge=1, le=128000)
    capabilities: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    max_iterations: int = Field(10, ge=1, le=100)


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    model: str
    provider: str
    capabilities: List[str]
    tools: List[str]


class AgentRunRequest(BaseModel):
    task: str = Field(..., description="Task for the agent to execute")
    context: Optional[Dict] = Field(None, description="Additional context")


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    page_size: tuple = Depends(get_pagination),
    role: Optional[str] = Query(None),
    user: str = Depends(verify_api_key),
):
    """List all registered agents."""
    agents = list(_agents.values())
    if role:
        agents = [a for a in agents if a.config.role.value == role]
    page, size = page_size
    start = (page - 1) * size
    return [
        AgentResponse(
            id=a.id,
            name=a.config.name,
            role=a.config.role.value,
            description=a.config.description,
            model=a.config.model,
            provider=a.config.provider,
            capabilities=a.config.capabilities,
            tools=a.config.tools,
        )
        for a in agents[start:start + size]
    ]


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    request: AgentCreateRequest,
    user: str = Depends(verify_api_key),
):
    """Create a new agent."""
    if request.name in _agents:
        raise HTTPException(status_code=409, detail=f"Agent '{request.name}' already exists")

    config = AgentConfig(
        name=request.name,
        role=AgentRole(request.role),
        description=request.description,
        system_prompt=request.system_prompt,
        model=request.model,
        provider=request.provider,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        capabilities=request.capabilities,
        tools=request.tools,
        max_iterations=request.max_iterations,
    )
    agent = Agent(config)
    _agents[request.name] = agent

    return AgentResponse(
        id=agent.id,
        name=agent.config.name,
        role=agent.config.role.value,
        description=agent.config.description,
        model=agent.config.model,
        provider=agent.config.provider,
        capabilities=agent.config.capabilities,
        tools=agent.config.tools,
    )


@router.get("/{agent_name}", response_model=AgentResponse)
async def get_agent(agent_name: str, user: str = Depends(verify_api_key)):
    """Get agent details."""
    agent = _agents.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return AgentResponse(
        id=agent.id, name=agent.config.name, role=agent.config.role.value,
        description=agent.config.description, model=agent.config.model,
        provider=agent.config.provider, capabilities=agent.config.capabilities,
        tools=agent.config.tools,
    )


@router.delete("/{agent_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_name: str, user: str = Depends(verify_api_key)):
    """Delete an agent."""
    if agent_name not in _agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    del _agents[agent_name]


@router.post("/{agent_name}/run")
async def run_agent(
    agent_name: str,
    request: AgentRunRequest,
    user: str = Depends(verify_api_key),
):
    """Execute a task with the agent."""
    agent = _agents.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    result = await agent.run(request.task, request.context)
    return result
