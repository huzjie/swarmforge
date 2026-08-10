"""V2 eval API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/evals", tags=["evals v2"])

@router.get("/")
async def list_evals():
    return {"version": "v2", "evals": []}

@router.get("/{id}")
async def get_eval(id: str):
    return {"version": "v2", "id": id}
