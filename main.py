from dotenv import load_dotenv
from fastapi import FastAPI

from routers import genres, movies, users, ratings, actions

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI()
app.include_router(genres.router)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)
app.include_router(actions.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FilmTinder API!"}
