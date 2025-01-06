from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class SlotType(str, Enum):
    GENERAL = "general"
    RACE = "race"
    BLOCKED = "blocked"

class TimeSlot(BaseModel):
    id: str = Field(default_factory=str)
    start_time: datetime
    end_time: datetime
    slot_type: SlotType
    price: float
    is_booked: bool = False
    blocked_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Booking(BaseModel):
    id: str = Field(default_factory=str)
    time_slot_id: str
    user_id: str
    payment_status: str
    payment_id: Optional[str]
    amount_paid: float
    booking_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "confirmed"  # confirmed, cancelled, completed

class Race(BaseModel):
    id: str = Field(default_factory=str)
    time_slot_id: str
    name: str
    max_participants: int
    current_participants: int = 0
    race_type: str
    entry_fee: float
    status: str = "open"  # open, full, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RaceParticipant(BaseModel):
    id: str = Field(default_factory=str)
    race_id: str
    user_id: str
    payment_status: str
    payment_id: Optional[str]
    registration_time: datetime = Field(default_factory=datetime.utcnow)