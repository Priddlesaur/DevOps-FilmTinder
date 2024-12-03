from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import MovieDto, MovieBaseDto
from helpers.database_helpers import delete_or_rollback, get_all_entities, get_entity, create_or_rollback, \
    update_or_rollback
from models.base import Movie

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.get("/", response_model=list[MovieDto])
async def read_movies(db: Session = Depends(get_db)):
    movies = get_all_entities(Movie, db)
    return [MovieDto.model_validate(movie) for movie in movies]

@router.get("/{movie_id}", response_model=MovieDto)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = get_entity(Movie,movie_id, db)
    return MovieDto.model_validate(movie)

@router.post("/", response_model=MovieDto)
async def create_movie(movie: MovieDto, response: Response, db: Session = Depends(get_db)):
    new_movie = create_or_rollback(Movie, movie.model_dump(), db)
    response.headers["Location"] = f"/genres/{new_movie.id}"
    return MovieDto.model_validate(new_movie)

@router.patch("/{movie_id}", response_model=MovieDto)
async def update_movie(movie_id: int, updated_movie: MovieBaseDto, db: Session = Depends(get_db)):
    movie = get_entity(Movie, movie_id, db)
    updates = updated_movie.model_dump(exclude_none=True)
    updated_movie_final = update_or_rollback(movie, updates, db)
    return MovieBaseDto.model_validate(updated_movie_final)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = get_entity(Movie, movie_id, db)
    delete_or_rollback(movie,db)
    return {"detail": f"Movie with ID {movie_id} has been deleted"}