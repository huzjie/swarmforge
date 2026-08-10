"""Api_key schema definitions."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class Api_keyBase(BaseModel):
    name: str = Field(..., description="Api_key name")
    description: Optional[str] = None

class Api_keyCreate(Api_keyBase):
    pass

class Api_keyResponse(Api_keyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
