"""V2 tool API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/tools", tags=["tools v2"])

@router.get("/")
async def list_tools():
    return {"version": "v2", "tools": []}

@router.get("/{id}")
async def get_tool(id: str):
    return {"version": "v2", "id": id}
