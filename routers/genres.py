from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import GenreDto
from models.base import Genre

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
)

@router.get("/")
async def read_genres(db: Session = Depends(get_db)):
    genres = db.query(Genre).all()
    if not genres:
        raise HTTPException(status_code=404, detail="No genres found")

    genre_dtos = []
    for genre in genres:
        genre_dtos.append(GenreDto.model_validate(genre))

    return genre_dtos

@router.get("/{genre_id}")
async def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Return the genre
    return GenreDto.model_validate(genre)
