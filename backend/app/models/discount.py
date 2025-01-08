from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DiscountCode(BaseModel):
    id: str = Field(default_factory=str)
    code: str
    discount_percentage: float
    max_uses: Optional[int]
    current_uses: int = 0
    valid_from: datetime
    valid_until: datetime
    is_active: bool = True
    created_by_admin: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)