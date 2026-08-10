"""V2 task API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/tasks", tags=["tasks v2"])

@router.get("/")
async def list_tasks():
    return {"version": "v2", "tasks": []}

@router.get("/{id}")
async def get_task(id: str):
    return {"version": "v2", "id": id}
