"""Workflow API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from swarmforge.api.deps import verify_api_key

router = APIRouter()
_workflows: Dict = {}

class WorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""
    steps: List[Dict] = Field(default_factory=list)

@router.get("/")
async def list_workflows(user: str = Depends(verify_api_key)):
    return list(_workflows.values())

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_workflow(request: WorkflowCreateRequest, user: str = Depends(verify_api_key)):
    _workflows[request.name] = request.model_dump()
    return _workflows[request.name]

@router.get("/{name}")
async def get_workflow(name: str, user: str = Depends(verify_api_key)):
    wf = _workflows.get(name)
    if not wf: raise HTTPException(status_code=404)
    return wf
