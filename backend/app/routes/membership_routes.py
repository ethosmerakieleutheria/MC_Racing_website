from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import List

from ..database import get_db
from ..models.membership import Membership, MembershipTier, MembershipBenefit

router = APIRouter()

@router.post("/membership/subscribe")
async def subscribe_membership(
    user_id: str,
    tier: MembershipTier,
    payment_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Subscribe to a membership tier"""
    # Check if user already has active membership
    existing_membership = await db.memberships.find_one({
        "user_id": user_id,
        "is_active": True,
        "end_date": {"$gt": datetime.utcnow()}
    })
    
    if existing_membership:
        raise HTTPException(status_code=400, detail="User already has active membership")
    
    # Create new membership
    membership = Membership(
        user_id=user_id,
        tier=tier,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=365),  # 1-year membership
        payment_status="completed",
        payment_id=payment_id
    )
    
    await db.memberships.insert_one(membership.dict())
    return {"message": "Successfully subscribed to membership"}