from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Admin(BaseModel):
    id: str = Field(default_factory=str)
    password_hash: str
    last_updated: datetime = Field(default_factory=datetime.utcnow)