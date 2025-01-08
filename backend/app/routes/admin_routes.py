from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List, Optional
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from ..database import get_db
from ..models.time_slots import TimeSlot, SlotType
from ..models.admin import Admin
from ..models.organizers import Organizer

router = APIRouter()

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminAuth(BaseModel):
    password: str

class TimeBlockRequest(BaseModel):
    password: str
    start_time: datetime
    end_time: datetime
    reason: str

class OrganizerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str  


async def verify_admin(password: str, db: AsyncIOMotorDatabase) -> bool:
    """Verify admin password against stored hash"""
    admin_doc = await db.admin.find_one({})
    if not admin_doc:
        raise HTTPException(status_code=404, detail="Admin account not configured")
    
    return pwd_context.verify(password, admin_doc["password_hash"])

@router.post("/admin/setup")
async def setup_admin(
    auth: AdminAuth,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Initial admin password setup - can only be done if no admin exists"""
    existing_admin = await db.admin.find_one({})
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already configured")
    
    # Hash the password
    password_hash = pwd_context.hash(auth.password)
    
    # Create admin document
    admin = Admin(
        password_hash=password_hash
    )
    
    await db.admin.insert_one(admin.dict())
    return {"message": "Admin account created successfully"}

@router.post("/admin/organizers/create")
async def create_organizer(
    admin_password: str,
    organizer_data: OrganizerCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new organizer (admin only)"""
    # Verify admin password
    if not await verify_admin(admin_password, db):
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    # Check if organizer already exists
    existing_organizer = await db.organizers.find_one({"email": organizer_data.email})
    if existing_organizer:
        raise HTTPException(status_code=400, detail="Organizer with this email already exists")
    
    # Create organizer with hashed password
    organizer = Organizer(
        first_name=organizer_data.first_name,
        last_name=organizer_data.last_name,
        email=organizer_data.email,
        phone=organizer_data.phone,
        password_hash=pwd_context.hash(organizer_data.password),
        created_by_admin=str((await db.admin.find_one({}))["_id"])
    )
    
    result = await db.organizers.insert_one(organizer.dict())
    
    return {
        "message": "Organizer created successfully",
        "organizer_id": str(result.inserted_id)
    }

@router.post("/admin/change-password")
async def change_admin_password(
    old_password: str,
    new_password: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Change admin password"""
    # Verify old password
    if not await verify_admin(old_password, db):
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    # Hash new password
    new_password_hash = pwd_context.hash(new_password)
    
    # Update password
    await db.admin.update_one(
        {},
        {
            "$set": {
                "password_hash": new_password_hash,
                "last_updated": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Admin password updated successfully"}

@router.post("/timeslots/block")
async def block_time_slot(
    block_request: TimeBlockRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Block a time slot (admin only)"""
    # Verify admin password
    if not await verify_admin(block_request.password, db):
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    # Validate time range
    if block_request.start_time >= block_request.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    # Check if slot is already blocked or booked
    existing_slot = await db.time_slots.find_one({
        "start_time": {"$lt": block_request.end_time},
        "end_time": {"$gt": block_request.start_time}
    })
    
    if existing_slot:
        raise HTTPException(status_code=400, detail="Time slot overlaps with existing slot")
    
    # Create blocked time slot
    time_slot = TimeSlot(
        start_time=block_request.start_time,
        end_time=block_request.end_time,
        slot_type=SlotType.BLOCKED,
        price=0,
        is_booked=True,
        blocked_reason=block_request.reason
    )
    
    result = await db.time_slots.insert_one(time_slot.dict())
    
    return {
        "message": "Time slot blocked successfully",
        "blocked_slot": {
            "id": str(result.inserted_id),
            "start_time": block_request.start_time.strftime("%m/%d/%Y %I:%M %p"),
            "end_time": block_request.end_time.strftime("%m/%d/%Y %I:%M %p"),
            "reason": block_request.reason
        }
    }

@router.get("/timeslots/blocked")
async def get_blocked_slots(
    admin_password: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all blocked time slots (admin only)"""
    # Verify admin password
    if not await verify_admin(admin_password, db):
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    # Get all blocked slots
    blocked_slots = await db.time_slots.find({
        "slot_type": "blocked"
    }).to_list(None)
    
    # Format response
    formatted_slots = []
    for slot in blocked_slots:
        formatted_slots.append({
            "id": str(slot["_id"]),
            "start_time": slot["start_time"].strftime("%m/%d/%Y %I:%M %p"),
            "end_time": slot["end_time"].strftime("%m/%d/%Y %I:%M %p"),
            "reason": slot.get("blocked_reason", "No reason provided"),
            "created_at": slot["created_at"].strftime("%m/%d/%Y %I:%M %p")
        })
    
    return {
        "total_blocked_slots": len(formatted_slots),
        "blocked_slots": formatted_slots
    }

@router.post("/admin/discounts/create")
async def create_discount_code(
    admin_password: str,
    code: str,
    discount_percentage: float,
    max_uses: Optional[int],
    valid_days: int,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create a new discount code"""
    if not await verify_admin(admin_password, db):
        raise HTTPException(status_code=401, detail="Invalid admin password")
    
    # Create discount code
    discount = DiscountCode(
        code=code.upper(),
        discount_percentage=discount_percentage,
        max_uses=max_uses,
        valid_from=datetime.utcnow(),
        valid_until=datetime.utcnow() + timedelta(days=valid_days),
        created_by_admin=str((await db.admin.find_one({}))["_id"])
    )
    
    await db.discount_codes.insert_one(discount.dict())
    return {"message": "Discount code created successfully"}