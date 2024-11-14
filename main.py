from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from routers import genres, movies

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI()
app.include_router(genres.router)
app.include_router(movies.router)

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
