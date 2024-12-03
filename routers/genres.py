from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import GenreDto, GenreBaseDto
from helpers.database_helpers import delete_or_rollback, get_all_entities, get_entity, create_or_rollback, \
    update_or_rollback
from models.base import Genre

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
)

@router.get("/", response_model=list[GenreDto])
async def read_genres(db: Session = Depends(get_db)):
    genres = get_all_entities(Genre, db)
    return [GenreDto.model_validate(genre) for genre in genres]

@router.get("/{genre_id}", response_model=GenreDto)
async def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = get_entity(Genre, genre_id, db)
    return GenreDto.model_validate(genre)

@router.post("/", status_code=201, response_model=GenreDto)
async def create_genre(genre: GenreBaseDto, response: Response, db: Session = Depends(get_db)):
    new_genre = create_or_rollback(Genre, genre.model_dump(), db)
    response.headers["Location"] = f"/genres/{new_genre.id}"
    return GenreDto.model_validate(new_genre)

@router.patch("/{genre_id}", response_model=GenreDto)
async def update_genre(genre_id: int, updated_genre: GenreBaseDto, db: Session = Depends(get_db)):
    genre = get_entity(Genre, genre_id, db)
    updates = updated_genre.model_dump(exclude_none=True)
    updated_genre_final = update_or_rollback(genre, updates, db)
    return GenreDto.model_validate(updated_genre_final)

@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = get_entity(Genre,genre_id, db)
    delete_or_rollback(genre, db)
    return {"message": f"Genre with ID {genre_id} has been deleted"}