from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List
from bson import ObjectId

from ..database import get_db
from ..models.training import TrainingSlot, TrainingRegistration
from ..models.shared import TimeSlotRequest, parse_datetime
from ..models.membership import Membership

router = APIRouter()

@router.post("/training/slots/create")
async def create_training_slot(
    admin_password: str,
    time_slot: TimeSlotRequest,
    max_trainees: int,
    trainer_id: str,
    price: float,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a training slot (admin only)"""
    # Admin verification logic here
    
    start_datetime = parse_datetime(time_slot.date, time_slot.start_time)
    end_datetime = parse_datetime(time_slot.date, time_slot.end_time)
    
    training_slot = TrainingSlot(
        start_time=start_datetime,
        end_time=end_datetime,
        max_trainees=max_trainees,
        trainer_id=trainer_id,
        price=price
    )
    
    result = await db.training_slots.insert_one(training_slot.dict())
    
    return {
        "message": "Training slot created successfully",
        "slot_id": str(result.inserted_id)
    }

@router.post("/training/register")
async def register_for_training(
    slot_id: str,
    user_id: str,
    payment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Register for a training slot"""
    # Check if user has active membership for discount
    membership = await db.memberships.find_one({
        "user_id": user_id,
        "is_active": True,
        "end_date": {"$gt": datetime.utcnow()}
    })
    
    training_slot = await db.training_slots.find_one({"_id": ObjectId(slot_id)})
    
    # Apply membership discount if applicable
    final_price = training_slot["price"]
    if membership:
        benefit = await db.membership_benefits.find_one({"tier": membership["tier"]})
        discount = benefit["training_discount"]
        final_price = training_slot["price"] * (1 - discount/100)
    
    registration = TrainingRegistration(
        user_id=user_id,
        slot_id=slot_id,
        payment_status="completed",
        payment_id=payment_id
    )
    
    await db.training_registrations.insert_one(registration.dict())
    
    return {"message": "Successfully registered for training"}