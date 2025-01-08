from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List

from ..database import get_db
from ..models.leaderboard import RaceResult, LeaderboardEntry

router = APIRouter()

@router.get("/leaderboard/top")
async def get_leaderboard(
    limit: int = 15,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get top members from leaderboard"""
    # Get only members
    member_ids = await db.memberships.distinct("user_id", {
        "is_active": True,
        "end_date": {"$gt": datetime.utcnow()}
    })
    
    # Get leaderboard entries for members
    leaderboard = await db.leaderboard_entries.find({
        "user_id": {"$in": member_ids}
    }).sort("total_points", -1).limit(limit).to_list(None)
    
    # Enrich with user details
    enriched_leaderboard = []
    for entry in leaderboard:
        user = await db.users.find_one({"_id": ObjectId(entry["user_id"])})
        enriched_leaderboard.append({
            "rank": len(enriched_leaderboard) + 1,
            "name": f"{user['first_name']} {user['last_name']}",
            "total_points": entry["total_points"],
            "total_races": entry["total_races"],
            "best_position": entry["best_position"]
        })
    
    return {
        "leaderboard": enriched_leaderboard
    }