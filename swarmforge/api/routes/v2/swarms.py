"""V2 swarm API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/swarms", tags=["swarms v2"])

@router.get("/")
async def list_swarms():
    return {"version": "v2", "swarms": []}

@router.get("/{id}")
async def get_swarm(id: str):
    return {"version": "v2", "id": id}
