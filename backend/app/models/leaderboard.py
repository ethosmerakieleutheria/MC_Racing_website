from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RaceResult(BaseModel):
    id: str = Field(default_factory=str)
    race_id: str
    user_id: str
    finish_time: datetime
    position: int
    points: int  # Points awarded based on position
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LeaderboardEntry(BaseModel):
    id: str = Field(default_factory=str)
    user_id: str
    total_points: int = 0
    total_races: int = 0
    best_position: int
    last_updated: datetime = Field(default_factory=datetime.utcnow)