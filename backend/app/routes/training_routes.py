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

@router.get("/slots")
async def get_training_slots(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Fetch all available training slots.
    """
    try:
        # Query for open training slots
        training_slots = await db.training_slots.find({"status": "open"}).to_list(length=100)

        # Format the response
        formatted_slots = [
            {
                "id": str(slot["_id"]),
                "name": slot.get("name", "Unnamed Training"),
                "date": slot.get("date"),
                "price": slot.get("price"),
                "level": slot.get("level"),
                "max_trainees": slot.get("max_trainees"),
                "current_trainees": slot.get("current_trainees"),
                "duration": slot.get("duration"),
                "trainer": slot.get("trainer"),
                "status": slot.get("status"),
            }
            for slot in training_slots
        ]

        return {
            "total_slots": len(formatted_slots),
            "training_slots": formatted_slots
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching training slots: {str(e)}"
        )

@router.post("/slots/create")
async def create_training_slot(
    admin_password: str,
    time_slot: TimeSlotRequest,
    max_trainees: int,
    trainer_id: str,
    price: float,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Create a training slot (admin only).
    """
    # Admin verification logic here (can be replaced with an actual auth system)

    start_datetime = parse_datetime(time_slot.date, time_slot.start_time)
    end_datetime = parse_datetime(time_slot.date, time_slot.end_time)

    # Create a training slot document
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

@router.post("/register")
async def register_for_training(
    slot_id: str,
    user_id: str,
    payment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Register for a training slot.
    """
    # Check if user has an active membership for discounts
    membership = await db.memberships.find_one({
        "user_id": user_id,
        "is_active": True,
        "end_date": {"$gt": datetime.utcnow()}
    })

    training_slot = await db.training_slots.find_one({"_id": ObjectId(slot_id)})
    if not training_slot:
        raise HTTPException(status_code=404, detail="Training slot not found")

    # Apply membership discount if applicable
    final_price = training_slot["price"]
    if membership:
        benefit = await db.membership_benefits.find_one({"tier": membership["tier"]})
        if benefit:
            discount = benefit["training_discount"]
            final_price = training_slot["price"] * (1 - discount / 100)

    # Register the user for the training slot
    registration = TrainingRegistration(
        user_id=user_id,
        slot_id=slot_id,
        payment_status="completed",
        payment_id=payment_id
    )

    await db.training_registrations.insert_one(registration.dict())

    return {
        "message": "Successfully registered for training",
        "final_price": final_price
    }
