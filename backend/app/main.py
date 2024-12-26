from fastapi import FastAPI, APIRouter

router = APIRouter()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("mcRacing")
async def mc_racing():
    return {"message": "Welcome to the MC Racing World!"}

