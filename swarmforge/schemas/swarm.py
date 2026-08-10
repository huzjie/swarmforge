"""Swarm schema definitions."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SwarmBase(BaseModel):
    name: str = Field(..., description="Swarm name")
    description: Optional[str] = None

class SwarmCreate(SwarmBase):
    pass

class SwarmResponse(SwarmBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
