from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MembershipTier(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

class MembershipBenefit(BaseModel):
    id: str = Field(default_factory=str)
    tier: MembershipTier
    race_discount: float  # Percentage discount on races
    training_discount: float  # Percentage discount on training
    general_slot_discount: float  # Percentage discount on general slots
    created_by_admin: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Membership(BaseModel):
    id: str = Field(default_factory=str)
    user_id: str
    tier: MembershipTier
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    payment_status: str
    payment_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)