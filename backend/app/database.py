from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
import asyncio
from .config import settings

class MongoEngine:
    def __init__(self, url: str, db_name: str):
        try:
            self.client = AsyncIOMotorClient(url)
            self.db = self.client[db_name]
        except Exception as e:
            print(f"Failed to initialize MongoDB connection: {e}")
            raise
        
    async def verify_connection(self):
        try:
            await self.db.command('ping')
            print("✅ Successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
        
    async def close(self):
        self.client.close()
        
    def get_db(self):
        return self.db

mongo_engine = MongoEngine(settings.mongodb_url, settings.database_name)        

async def get_db():
    """Dependency for getting database instance"""
    try:
        db = mongo_engine.get_db()
        await mongo_engine.verify_connection()  # Verify connection is alive
        yield db
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")