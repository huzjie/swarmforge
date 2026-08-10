"""
Tool management API endpoints.
"""
from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel

from swarmforge.api.deps import verify_api_key
from swarmforge.core.tool import registry

router = APIRouter()


class ToolInfo(BaseModel):
    name: str
    description: str
    parameters: List[dict]


@router.get("/", response_model=List[ToolInfo])
async def list_tools(user: str = Depends(verify_api_key)):
    tools = registry.list()
    return [
        ToolInfo(
            name=t.name,
            description=t.description,
            parameters=[
                {"name": p.name, "type": p.type, "description": p.description, "required": p.required}
                for p in t.parameters
            ],
        )
        for t in tools
    ]


@router.get("/schemas/openai")
async def get_openai_schemas(user: str = Depends(verify_api_key)):
    return registry.get_openai_schemas()


@router.get("/schemas/anthropic")
async def get_anthropic_schemas(user: str = Depends(verify_api_key)):
    return registry.get_anthropic_schemas()
