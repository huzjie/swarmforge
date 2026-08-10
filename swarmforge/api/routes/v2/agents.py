"""V2 agent API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/agents", tags=["agents v2"])

@router.get("/")
async def list_agents():
    return {"version": "v2", "agents": []}

@router.get("/{id}")
async def get_agent(id: str):
    return {"version": "v2", "id": id}
