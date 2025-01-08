from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class Organizer(BaseModel):
    id: str = Field(default_factory=str)
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password_hash: str
    is_active: bool = True
    created_by_admin: str  # Admin ID who created this organizer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)