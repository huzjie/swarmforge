"""V2 metrics API endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/v2/metricss", tags=["metricss v2"])

@router.get("/")
async def list_metricss():
    return {"version": "v2", "metricss": []}

@router.get("/{id}")
async def get_metrics(id: str):
    return {"version": "v2", "id": id}
