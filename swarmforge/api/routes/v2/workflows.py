"""V2 workflow API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/workflows", tags=["workflows v2"])

@router.get("/")
async def list_workflows():
    return {"version": "v2", "workflows": []}

@router.get("/{id}")
async def get_workflow(id: str):
    return {"version": "v2", "id": id}
