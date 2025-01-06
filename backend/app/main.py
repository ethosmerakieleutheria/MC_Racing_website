from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .database import mongo_engine
from .routes import booking_routes, view_routes, user_routes, admin_routes

app = FastAPI(title="MC Racing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.on_event("startup")
async def startup_db():
    try:
        # Verify database connection
        await mongo_engine.verify_connection()
        
        # Initialize collections and indexes
        db = mongo_engine.get_db()
        await db.admin.create_index("last_updated")
        await db.time_slots.create_index([("start_time", 1), ("end_time", 1)])
        await db.time_slots.create_index([("slot_type", 1)])
        
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db():
    await mongo_engine.close()

# Include routers
app.include_router(booking_routes.router, prefix="/api/v1", tags=["bookings"])
app.include_router(view_routes.router, prefix="/api/v1", tags=["views"])
app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])
app.include_router(admin_routes.router, prefix="/api/v1", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "MC Racing API is running!"}