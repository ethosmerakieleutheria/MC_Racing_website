# app/routes/contact_routes.py
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..database import get_db
from pydantic import BaseModel, EmailStr
from datetime import datetime

router = APIRouter()

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

@router.post("/contact")
async def send_message(
    message: ContactMessage,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    try:
        contact_message = {
            "name": message.name,
            "email": message.email,
            "message": message.message,
            "created_at": datetime.utcnow(),
            "status": "unread"
        }
        
        result = await db.contact_messages.insert_one(contact_message)
        
        # Here you could also add email notification logic
        
        return {
            "message": "Message sent successfully",
            "message_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))