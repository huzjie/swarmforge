"""V2 admin API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/admins", tags=["admins v2"])

@router.get("/")
async def list_admins():
    return {"version": "v2", "admins": []}

@router.get("/{id}")
async def get_admin(id: str):
    return {"version": "v2", "id": id}
