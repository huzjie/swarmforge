"""Evaluation API endpoints."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from swarmforge.api.deps import verify_api_key

router = APIRouter()
_eval_results: List[Dict] = []

class EvalRequest(BaseModel):
    agent_name: str
    test_cases: List[Dict] = Field(default_factory=list)

@router.post("/")
async def run_evaluation(request: EvalRequest, user: str = Depends(verify_api_key)):
    result = {"agent": request.agent_name, "tests": len(request.test_cases), "status": "completed"}
    _eval_results.append(result)
    return result

@router.get("/")
async def list_evaluations(user: str = Depends(verify_api_key)):
    return _eval_results
