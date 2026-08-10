"""Metrics API endpoints."""
from fastapi import APIRouter, Depends
from swarmforge.api.deps import verify_api_key
from swarmforge.monitoring.metrics import (
    agent_runs_total, swarm_runs_total, api_requests_total
)

router = APIRouter()

@router.get("/summary")
async def metrics_summary(user: str = Depends(verify_api_key)):
    return {
        "agents": {"runs": "see /metrics endpoint for Prometheus data"},
        "swarms": {"runs": "see /metrics endpoint for Prometheus data"},
        "api": {"requests": "see /metrics endpoint for Prometheus data"},
    }
