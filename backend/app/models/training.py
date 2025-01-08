from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TrainingSlot(BaseModel):
    id: str = Field(default_factory=str)
    start_time: datetime
    end_time: datetime
    max_trainees: int
    current_trainees: int = 0
    trainer_id: str  # Reference to organizer who will conduct training
    price: float
    is_available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TrainingRegistration(BaseModel):
    id: str = Field(default_factory=str)
    user_id: str
    slot_id: str
    payment_status: str
    payment_id: Optional[str]
    registration_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, confirmed, completed, cancelled