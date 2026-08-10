"""
Swarm management API endpoints.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from swarmforge.api.deps import verify_api_key
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology
from swarmforge.core.agent import AgentConfig, AgentRole

router = APIRouter()

_swarms: Dict[str, Swarm] = {}


class SwarmCreateRequest(BaseModel):
    name: str
    topology: str = "parallel"
    max_concurrent_agents: int = Field(10, ge=1, le=100)
    global_timeout_seconds: int = Field(600, ge=10, le=3600)
    agent_configs: List[Dict] = Field(default_factory=list, description="List of agent configs")


class SwarmRunRequest(BaseModel):
    task: str
    context: Optional[Dict] = None


@router.get("/")
async def list_swarms(user: str = Depends(verify_api_key)):
    return [
        {"name": s.config.name, "topology": s.config.topology.value, "agents": len(s.agents)}
        for s in _swarms.values()
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_swarm(request: SwarmCreateRequest, user: str = Depends(verify_api_key)):
    if request.name in _swarms:
        raise HTTPException(status_code=409, detail=f"Swarm '{request.name}' already exists")

    config = SwarmConfig(
        name=request.name,
        topology=SwarmTopology(request.topology),
        max_concurrent_agents=request.max_concurrent_agents,
        global_timeout_seconds=request.global_timeout_seconds,
    )
    swarm = Swarm(config)

    for ac in request.agent_configs:
        agent_config = AgentConfig(
            name=ac.get("name", f"agent-{len(swarm.agents)}"),
            role=AgentRole(ac.get("role", "worker")),
            description=ac.get("description", ""),
            system_prompt=ac.get("system_prompt", ""),
            model=ac.get("model", "gpt-4"),
            provider=ac.get("provider", "openai"),
            capabilities=ac.get("capabilities", []),
            tools=ac.get("tools", []),
            max_iterations=ac.get("max_iterations", 10),
        )
        from swarmforge.core.agent import Agent
        swarm.add_agent(Agent(agent_config))

    _swarms[request.name] = swarm
    return {"name": request.name, "agents": len(swarm.agents), "topology": config.topology.value}


@router.get("/{swarm_name}")
async def get_swarm(swarm_name: str, user: str = Depends(verify_api_key)):
    swarm = _swarms.get(swarm_name)
    if not swarm:
        raise HTTPException(status_code=404, detail=f"Swarm '{swarm_name}' not found")
    return swarm.get_stats()


@router.delete("/{swarm_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_swarm(swarm_name: str, user: str = Depends(verify_api_key)):
    if swarm_name not in _swarms:
        raise HTTPException(status_code=404)
    del _swarms[swarm_name]


@router.post("/{swarm_name}/run")
async def run_swarm(swarm_name: str, request: SwarmRunRequest, user: str = Depends(verify_api_key)):
    swarm = _swarms.get(swarm_name)
    if not swarm:
        raise HTTPException(status_code=404)
    run = await swarm.run(request.task, request.context)
    return {
        "run_id": run.id,
        "status": run.status,
        "results": run.results,
        "errors": run.errors,
    }
