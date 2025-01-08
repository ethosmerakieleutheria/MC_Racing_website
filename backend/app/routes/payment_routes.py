# app/routes/payment_routes.py
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..database import get_db
from ..payment.stripe_config import create_payment_intent
from pydantic import BaseModel

router = APIRouter()

class PaymentIntentRequest(BaseModel):
    race_id: str

@router.post("/payment/create-intent")
async def create_payment_intent_endpoint(
    request: PaymentIntentRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    try:
        # Get race details to determine amount
        race = await db.races.find_one({"_id": ObjectId(request.race_id)})
        if not race:
            raise HTTPException(status_code=404, detail="Race not found")

        # Create Stripe payment intent
        amount = int(race["entry_fee"] * 100)  # Convert to cents
        intent = await create_payment_intent(amount)
        
        return {
            "clientSecret": intent.client_secret,
            "amount": amount,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))