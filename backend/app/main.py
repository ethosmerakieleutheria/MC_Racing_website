from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .database import mongo_engine

from fastapi.middleware.cors import CORSMiddleware

# Add this after creating the FastAPI app


# Import all route modules
from .routes import (
    booking_routes, 
    view_routes, 
    user_routes, 
    admin_routes, 
    organizer_routes,
    training_routes,     # Add this import
    leaderboard_routes,  # Add this import
    membership_routes    # Add this import
)

app = FastAPI(title="MC Racing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CORS middleware configuration remains the same...

@app.on_event("startup")
async def startup_db():
    try:
        # Verify database connection
        await mongo_engine.verify_connection()
        
        # Initialize collections and indexes
        db = mongo_engine.get_db()
        
        # Existing indexes
        await db.admin.create_index("last_updated")
        await db.organizers.create_index("email", unique=True)
        await db.time_slots.create_index([("start_time", 1), ("end_time", 1)])
        await db.time_slots.create_index([("slot_type", 1)])
        await db.bookings.create_index([("customer_email", 1)])
        await db.bookings.create_index([("status", 1)])
        await db.race_registrations.create_index([("race_id", 1), ("user_id", 1)], unique=True)
        
        # New indexes for training, membership, leaderboard, and discounts
        await db.training_slots.create_index([("start_time", 1), ("end_time", 1)])
        await db.training_slots.create_index([("trainer_id", 1)])
        await db.training_registrations.create_index([("user_id", 1)])
        await db.training_registrations.create_index([("slot_id", 1)])
        
        await db.memberships.create_index([("user_id", 1), ("is_active", 1)])
        await db.memberships.create_index([("end_date", 1)])
        
        await db.leaderboard_entries.create_index([("total_points", -1)])
        await db.leaderboard_entries.create_index([("user_id", 1)])
        
        await db.discount_codes.create_index("code", unique=True)
        await db.discount_codes.create_index([("valid_until", 1)])
        
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        raise

# Include all routers
app.include_router(booking_routes.router, prefix="/api/v1", tags=["bookings"])
app.include_router(view_routes.router, prefix="/api/v1", tags=["views"])
app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])
app.include_router(admin_routes.router, prefix="/api/v1", tags=["admin"])
app.include_router(organizer_routes.router, prefix="/api/v1", tags=["organizers"])
app.include_router(training_routes.router, prefix="/api/v1", tags=["training"])      # Add this line
app.include_router(leaderboard_routes.router, prefix="/api/v1", tags=["leaderboard"]) # Add this line
app.include_router(membership_routes.router, prefix="/api/v1", tags=["membership"])   # Add this line

@app.get("/")
async def root():
    return {"message": "MC Racing API is running!"}