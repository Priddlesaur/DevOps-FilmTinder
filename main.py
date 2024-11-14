from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI()

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
