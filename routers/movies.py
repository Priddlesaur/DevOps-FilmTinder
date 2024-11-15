from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import MovieDto
from models.base import Movie

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.get("/", response_model=MovieDto)
async def read_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")

    movies_dtos = []
    for movie in movies:
        movies_dtos.append(MovieDto.model_validate(movie))

    # Return the movies
    return movies_dtos

@router.get("/{movie_id}", response_model=MovieDto)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Return the movie
    return MovieDto.model_validate(movie)

@router.post("/", response_model=MovieDto)
async def create_movie(movie: MovieDto):
