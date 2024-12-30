from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings


class MongoEngine:
    def __init__(self, url:str, db_name:str):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client[db_name]
        
    async def close(self):
        self.client.close()
        
    def get_db(self):
        return self.db
    
mongo_engine = MongoEngine(settings.mongodb_url, settings.database_name)        

async def get_db():
    db = mongo_engine.get_db()
    try:
        yield db
    except Exception as e:
        print(e)
    finally:
        pass