from alembic.config import Config
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, DATABASE_URL
from routers import genres, movies, users, ratings
from alembic import command

# Load environment variables
load_dotenv()

# Run alembic upgrade head to apply migrations
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
command.upgrade(alembic_cfg, "head")

# Create FastAPI instance
app = FastAPI()
app.include_router(genres.router)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
