"""Team schema definitions."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TeamBase(BaseModel):
    name: str = Field(..., description="Team name")
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
