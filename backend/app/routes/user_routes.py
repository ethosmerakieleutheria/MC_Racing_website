from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel

from ..database import get_db
from ..models.users import User

router = APIRouter()

class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: str  # Format: MM/DD/YYYY
    license_number: str
    emergency_contact_name: str
    emergency_contact_phone: str

@router.post("/users/register")
async def register_user(
    user_data: UserRegistration,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Register a new user"""
    try:
        # Validate date format
        try:
            dob = datetime.strptime(user_data.date_of_birth, '%m/%d/%Y')
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Date of birth must be in MM/DD/YYYY format"
            )

        # Check if user already exists
        existing_user = await db.users.find_one({
            "$or": [
                {"email": user_data.email},
                {"license_number": user_data.license_number}
            ]
        })
        
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail="User with this email or license number already exists"
            )

        # Create user document
        user_dict = {
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "phone": user_data.phone,
            "date_of_birth": dob,
            "license_number": user_data.license_number,
            "emergency_contact_name": user_data.emergency_contact_name,
            "emergency_contact_phone": user_data.emergency_contact_phone,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        
        result = await db.users.insert_one(user_dict)
        
        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))