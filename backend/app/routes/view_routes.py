from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import List

from ..database import get_db

router = APIRouter()

@router.get("/races")
async def get_all_races(db: AsyncIOMotorDatabase = Depends(get_db)):
    races = await db.races.find().to_list(length=100)
    return {"total_races": len(races), "races": races}


@router.get("/timeslots/available")
async def get_available_slots(
    start_date: datetime,
    end_date: datetime,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all available time slots between two dates"""
    slots = await db.time_slots.find({
        "start_time": {"$gte": start_date, "$lte": end_date},
        "is_booked": False,
        "slot_type": {"$ne": "blocked"}
    }).to_list(None)
    
    return slots

@router.get("/races/upcoming")
async def get_upcoming_races(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all upcoming races"""
    current_time = datetime.utcnow()
    
    races = await db.races.find({
        "status": "open",
        "start_time": {"$gt": current_time}
    }).to_list(None)
    
    return races

@router.get("/races/{race_id}/participants")
async def get_race_participants(
    race_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get participants for a specific race"""
    participants = await db.race_participants.find({
        "race_id": race_id
    }).to_list(None)
    
    return participants