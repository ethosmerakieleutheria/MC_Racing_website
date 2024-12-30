from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import mongo_engine

router = APIRouter()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db():
    # Initialize collections, indexes, etc.
    db = mongo_engine.get_db()
    await db.users.create_index("email", unique=True)

@app.on_event("shutdown")
async def shutdown_db():
    await mongo_engine.close()

#app.include_router(mc_racing_router.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/mcRacing")
async def mc_racing():
    return {"message": "Welcome to the MC Racing World!"}

