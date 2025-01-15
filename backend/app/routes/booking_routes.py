from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import List
import pytz
from pydantic import BaseModel, validator, EmailStr
from bson import ObjectId

from ..database import get_db
from ..models.time_slots import TimeSlot, Booking, Race, RaceParticipant, SlotType
from ..models.users import User


router = APIRouter()

def validate_object_id(id_str: str, field_name: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name} format. Must be a 24-character hex string."
        )

class TimeSlotRequest(BaseModel):
    date: str  # Format: MM/DD/YYYY
    start_time: str  # Format: HH:MM PM/AM
    end_time: str  # Format: HH:MM PM/AM
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%m/%d/%Y')
            return v
        except ValueError:
            raise ValueError('Date must be in MM/DD/YYYY format')
    
    @validator('start_time', 'end_time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%I:%M %p')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM PM/AM format (e.g., 02:30 PM)')

def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Convert date and time strings to datetime object"""
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    time_obj = datetime.strptime(time_str, '%I:%M %p').time()
    return datetime.combine(date_obj, time_obj)

@router.post("/races/create")
async def create_race(
    name: str,
    time_slot: TimeSlotRequest,
    max_participants: int,
    entry_fee: float,
    race_type: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new race event"""
    start_datetime = parse_datetime(time_slot.date, time_slot.start_time)
    end_datetime = parse_datetime(time_slot.date, time_slot.end_time)
    
    if start_datetime >= end_datetime:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    # Check if slot is available
    existing_slot = await db.time_slots.find_one({
        "start_time": {"$lt": end_datetime},
        "end_time": {"$gt": start_datetime}
    })
    
    if existing_slot:
        raise HTTPException(status_code=400, detail="Time slot not available")
    
    # Create time slot for race
    time_slot_doc = TimeSlot(
        start_time=start_datetime,
        end_time=end_datetime,
        slot_type=SlotType.RACE,
        price=entry_fee,
        is_booked=True
    )
    
    slot_result = await db.time_slots.insert_one(time_slot_doc.dict())
    
    # Create race
    race = Race(
        time_slot_id=str(slot_result.inserted_id),
        name=name,
        max_participants=max_participants,
        race_type=race_type,
        entry_fee=entry_fee
    )
    
    race_result = await db.races.insert_one(race.dict())
    
    return {
        "message": "Race created successfully",
        "race_id": str(race_result.inserted_id),
        "race_details": {
            "name": name,
            "date": time_slot.date,
            "start_time": time_slot.start_time,
            "end_time": time_slot.end_time,
            "max_participants": max_participants,
            "entry_fee": entry_fee
        }
    }


# Helper function to validate ObjectId
def validate_object_id(id_str: str, field_name: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name} format. Must be a 24-character hex string."
        )

@router.post("/races/{race_id}/join")
async def join_race(
    race_id: str,
    user_id: str,
    payment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Join an existing race"""
    # Convert string IDs to ObjectId
    race_object_id = validate_object_id(race_id, "race_id")
    user_object_id = validate_object_id(user_id, "user_id")
    
    # Validate user exists and is eligible
    user = await db.users.find_one({"_id": user_object_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.get("is_active"):
        raise HTTPException(status_code=400, detail="User account is not active")
    
    # Validate user's license
    if not user.get("license_number"):
        raise HTTPException(
            status_code=400, 
            detail="User must have a valid license to participate in races"
        )
    
    # Find race using ObjectId
    race = await db.races.find_one({"_id": race_object_id})
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    
    if race["current_participants"] >= race["max_participants"]:
        raise HTTPException(status_code=400, detail="Race is full")
    
    if race["status"] != "open":
        raise HTTPException(status_code=400, detail="Race is not open for registration")
    
    # Check if user already registered
    existing_participant = await db.race_participants.find_one({
        "race_id": race_id,
        "user_id": user_id
    })
    
    if existing_participant:
        raise HTTPException(status_code=400, detail="Already registered for this race")
    
    # Register participant
    participant = RaceParticipant(
        race_id=race_id,
        user_id=user_id,
        payment_status="completed",
        payment_id=payment_id
    )
    
    await db.race_participants.insert_one(participant.dict())
    
    # Update race participant count
    await db.races.update_one(
        {"_id": ObjectId(race_id)},
        {
            "$inc": {"current_participants": 1},
            "$set": {
                "status": "full" if race["current_participants"] + 1 >= race["max_participants"] else "open"
            }
        }
    )
    
    return {
        "message": "Successfully joined the race",
        "race_details": {
            "race_id": race_id,
            "race_name": race["name"],
            "participant_number": race["current_participants"] + 1
        }
    }


@router.post("/races/create")
async def create_race(
    name: str,
    max_participants: int,
    entry_fee: float,
    race_type: str,
    time_slot: TimeSlotRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new race event with date validation"""
    try:
        # Convert string dates to datetime objects
        start_datetime = parse_datetime(time_slot.date, time_slot.start_time)
        end_datetime = parse_datetime(time_slot.date, time_slot.end_time)
        
        # Validate dates
        current_time = datetime.utcnow()
        if start_datetime <= current_time:
            raise HTTPException(
                status_code=400, 
                detail="Race start time must be in the future"
            )
            
        if start_datetime >= end_datetime:
            raise HTTPException(
                status_code=400, 
                detail="End time must be after start time"
            )
        
        # Create the race document
        race_document = {
            "name": name,
            "start_time": start_datetime,
            "end_time": end_datetime,
            "max_participants": max_participants,
            "current_participants": 0,
            "race_type": race_type,
            "entry_fee": entry_fee,
            "status": "open",
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
                "entry_fee": entry_fee
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create race: {str(e)}")



@router.get("/races")
async def list_races(
    show_past: bool = True,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """List all races with an option to include past races"""
    try:
        # Get the current time
        current_time = datetime.utcnow()

        # Build the query based on parameters
        if show_past:
            query = {}
        else:
            query = {
                "date": {"$gte": current_time.strftime("%Y-%m-%d")}  # Compare as strings
            }

        # Find races based on query
        races = await db.races.find(query).to_list(None)

        # Format the response
        formatted_races = []
        for race in races:
            formatted_races.append({
                "id": str(race["_id"]),
                "name": race["name"],
                "date": race["date"],
                "price": race["price"],
                "level": race["level"],
                "max_participants": race["max_participants"],
                "current_participants": race["current_participants"],
                "status": race["status"],
                "race_type": race["race_type"]
            })

        return {
            "total_races": len(formatted_races),
            "races": formatted_races,
            "note": "Showing all races." if show_past else "Showing only future races."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch races: {str(e)}")


    
@router.post("/timeslots/book")
async def book_general_slot(
    time_slot: TimeSlotRequest,
    customer_name: str,
    customer_email: EmailStr,
    customer_phone: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Book a general driving slot (no registration required)"""
    start_datetime = parse_datetime(time_slot.date, time_slot.start_time)
    end_datetime = parse_datetime(time_slot.date, time_slot.end_time)
    
    # Validate dates
    current_time = datetime.utcnow()
    if start_datetime <= current_time:
        raise HTTPException(status_code=400, detail="Booking time must be in the future")
    
    if start_datetime >= end_datetime:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    # Check if slot is available
    existing_slot = await db.time_slots.find_one({
        "start_time": {"$lt": end_datetime},
        "end_time": {"$gt": start_datetime}
    })
    
    if existing_slot:
        raise HTTPException(status_code=400, detail="Time slot not available")
    
    # Create booking
    booking = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_phone": customer_phone,
        "start_time": start_datetime,
        "end_time": end_datetime,
        "booking_type": "general",
        "status": "pending_payment",
        "created_at": current_time
    }
    
    result = await db.bookings.insert_one(booking)
    
    return {
        "message": "Booking created successfully",
        "booking_id": str(result.inserted_id),
        "status": "pending_payment",
        "next_steps": "Please complete payment to confirm your booking"
    }

@router.post("/races/{race_id}/register")
async def register_for_race(
    race_id: str,
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Register intent to participate in a race (requires user account)"""
    # Validate race and user exist
    race = await db.races.find_one({"_id": ObjectId(race_id)})
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create race registration
    registration = {
        "race_id": race_id,
        "user_id": user_id,
        "status": "pending_payment",
        "created_at": datetime.utcnow()
    }
    
    result = await db.race_registrations.insert_one(registration)
    
    return {
        "message": "Race registration pending",
        "registration_id": str(result.inserted_id),
        "entry_fee": race["entry_fee"],
        "next_steps": "Please complete payment to confirm your participation"
    }