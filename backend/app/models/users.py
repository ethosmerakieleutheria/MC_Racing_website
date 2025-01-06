from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: str = Field(default_factory=str)
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: datetime
    license_number: str
    emergency_contact_name: str
    emergency_contact_phone: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True