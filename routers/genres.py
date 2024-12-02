from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import GenreDto, GenreBaseDto
from models.base import Genre

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
)

def try_get_genre(genre_id: int, db: Session) -> Genre:
    """
    Helperfunction for retreiving an existing genre by ID or throwing a 404-error.
    """
    genre = db.query(Genre).get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@router.get("/", response_model=list[GenreDto])
async def read_genres(db: Session = Depends(get_db)):
    """
    Retrieve all genres.
    """
    genres = db.query(Genre).all()
    if not genres:
        raise HTTPException(status_code=404, detail="No genres found")

    return [GenreDto.model_validate(genre) for genre in genres]

@router.get("/{genre_id}", response_model=GenreDto)
async def read_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Retrieve genre by ID.
    """
    genre = try_get_genre(genre_id, db)

    return GenreDto.model_validate(genre)

@router.post("/", status_code=201, response_model=GenreDto)
async def create_genre(genre: GenreBaseDto, response: Response, db: Session = Depends(get_db)):
    """
    Create a new genre.
    """
    new_genre = Genre(**genre.model_dump())

    # Try to add the new genre to the database
    try:
        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

    response.headers["Location"] = f"/genres/{new_genre.id}"

    # Return the new genre
    return GenreDto.model_validate(new_genre)

@router.patch("/{genre_id}", response_model=GenreDto)
async def update_genre(genre_id: int, updated_genre: GenreBaseDto, db: Session = Depends(get_db)):
    """
    Update an existing genre by ID.
    """
    genre = try_get_genre(genre_id, db)

    updates = updated_genre.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields for update")

    # Update the genre based on provided fields
    for key, value in updates.items():
        setattr(genre, key, value)

    # Commit changes and handle potential errors
    db.commit()
    db.refresh(genre)

    # Return the updated genre
    return GenreDto.model_validate(genre)

@router.delete("/{genre_id}")
async def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Delete a genre by ID.
    """
    genre = try_get_genre(genre_id, db)

    # Delete the genre from the database
    db.delete(genre)
    db.commit()

    # Return a message
    return {"message": f"Genre with {genre_id} has been deleted"}