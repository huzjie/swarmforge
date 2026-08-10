"""
Task queue and execution endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from swarmforge.api.deps import verify_api_key

router = APIRouter()

_tasks: Dict[str, Dict] = {}


class TaskSubmitRequest(BaseModel):
    task: str
    swarm_name: Optional[str] = None
    agent_name: Optional[str] = None
    priority: int = Field(0, ge=0, le=10)
    metadata: Dict = Field(default_factory=dict)


@router.get("/")
async def list_tasks(user: str = Depends(verify_api_key)):
    return list(_tasks.values())


@router.post("/")
async def submit_task(request: TaskSubmitRequest, user: str = Depends(verify_api_key)):
    import uuid, time
    task_id = str(uuid.uuid4())[:8]
    _tasks[task_id] = {
        "id": task_id,
        "task": request.task,
        "swarm_name": request.swarm_name,
        "agent_name": request.agent_name,
        "priority": request.priority,
        "status": "pending",
        "created_at": time.time(),
    }
    return _tasks[task_id]


@router.get("/{task_id}")
async def get_task(task_id: str, user: str = Depends(verify_api_key)):
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404)
    return task
