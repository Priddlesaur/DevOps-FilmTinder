from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import GenreDto, GenreBaseDto
from models.base import Genre

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
)

@router.get("/", response_model=list[GenreDto])
async def read_genres(db: Session = Depends(get_db)):
    genres = db.query(Genre).all()
    if not genres:
        raise HTTPException(status_code=404, detail="No genres found")

    genre_dtos = []
    for genre in genres:
        genre_dtos.append(GenreDto.model_validate(genre))

    return genre_dtos

@router.get("/{genre_id}", response_model=GenreDto)
async def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    return GenreDto.model_validate(genre)

@router.post("/", status_code=201, response_model=GenreDto)
async def create_genre(genre: GenreBaseDto, response: Response, db: Session = Depends(get_db)):
    new_genre = Genre(**genre.model_dump())

    # Try to add the new genre to the database
    try:
        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

    # Set the response status code to 201
    response.status_code = 201
    response.headers["Location"] = f"/genres/{new_genre.id}"

    # Return the new genre
    return GenreDto.model_validate(new_genre)

@router.patch("/{genre_id}", response_model=GenreDto)
async def update_genre(genre_id: int, updated_genre: GenreBaseDto, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter_by(id=genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Update the genre based on provided fields
    for key, value in updated_genre.model_dump(exclude_none=True).items():
        setattr(genre, key, value)

    # Commit changes and handle potential errors
    db.commit()

    # Return the updated genre
    return GenreDto.model_validate(genre)

@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    # Delete the genre from the database
    db.delete(genre)
    db.commit()

    # Return a message
    return {"message": f"Genre with {genre_id} has been deleted"}