from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from pydantic import BaseModel
from passlib.context import CryptContext

from ..database import get_db
from ..models.time_slots import TimeSlot, SlotType

from .booking_routes import TimeSlotRequest, parse_datetime

router = APIRouter()

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class OrganizerAuth(BaseModel):
    email: str
    password: str

async def verify_organizer(email: str, password: str, db: AsyncIOMotorDatabase) -> dict:
    """Verify organizer credentials and return organizer document"""
    organizer = await db.organizers.find_one({"email": email})
    if not organizer:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not pwd_context.verify(password, organizer["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not organizer["is_active"]:
        raise HTTPException(status_code=401, detail="Organizer account is inactive")
    
    return organizer

@router.post("/races/create")
async def create_race(
    auth: OrganizerAuth,
    time_slot: TimeSlotRequest,
    name: str,
    max_participants: int,
    entry_fee: float,
    race_type: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new race (organizer only)"""
    # Verify organizer
    organizer = await verify_organizer(auth.email, auth.password, db)
    
    # Convert string dates to datetime objects
    start_datetime = parse_datetime(time_slot.date, time_slot.start_time)
    end_datetime = parse_datetime(time_slot.date, time_slot.end_time)
    
    # Validate dates
    current_time = datetime.utcnow()
    if start_datetime <= current_time:
        raise HTTPException(status_code=400, detail="Race start time must be in the future")
    
    if start_datetime >= end_datetime:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    # Create race document
    race_document = {
        "name": name,
        "start_time": start_datetime,
        "end_time": end_datetime,
        "max_participants": max_participants,
        "current_participants": 0,
        "race_type": race_type,
        "entry_fee": entry_fee,
        "status": "open",
        "created_by": str(organizer["_id"]),
        "created_at": current_time
    }
    
    result = await db.races.insert_one(race_document)
    
    return {
        "message": "Race created successfully",
        "race_id": str(result.inserted_id),
        "race_details": {
            "name": name,
            "start_time": start_datetime.strftime("%m/%d/%Y %I:%M %p"),
            "end_time": end_datetime.strftime("%m/%d/%Y %I:%M %p"),
            "max_participants": max_participants,
            "entry_fee": entry_fee,
            "created_by": f"{organizer['first_name']} {organizer['last_name']}"
        }
    }