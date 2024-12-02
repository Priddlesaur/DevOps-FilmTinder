from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import MovieDto, MovieBaseDto
from models.base import Movie

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

def try_get_movie(movie_id: int, db: Session) -> Movie:
    """
    Helperfunction for retreiving an existing movie by ID or throwing a 404-error.
    """
    movie = db.query(Movie).get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/", response_model=list[MovieDto])
async def read_movies(db: Session = Depends(get_db)):
    """
    Retreive all movies.
    """
    movies = db.query(Movie).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")

    return [MovieDto.model_validate(movie) for movie in movies]

@router.get("/{movie_id}", response_model=MovieDto)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Retreive movie by ID.
    """
    movie = try_get_movie(movie_id, db)

    return MovieDto.model_validate(movie)

@router.post("/", response_model=MovieDto)
async def create_movie(movie: MovieDto, response: Response, db: Session = Depends(get_db)):
    """
    Create a new movie.
    """
    new_movie = Movie(**movie.model_dump())

    try:
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

    except IntegrityError as err:
        db.rollback()

        if "foreign key constraint" in str(err.orig).lower():
            raise HTTPException(status_code=400, detail="Invalid foreign key value")
        raise HTTPException(status_code=400, detail="Database constraint error")

    except KeyError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid field: {str(err)}")

    response.headers["Location"] = f"/genres/{new_movie.id}"

    return MovieDto.model_validate(new_movie)

@router.patch("/{movie_id}", response_model=MovieDto)
async def update_movie(movie_id: int, updated_movie: MovieBaseDto, db: Session = Depends(get_db)):
    """
    Update an existing movie by ID.
    """
    movie = try_get_movie(movie_id, db)

    try:
        update_data = updated_movie.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(movie, key, value)

        db.commit()
        db.refresh(movie)

    except IntegrityError as err:
        db.rollback()

        if "foreign key constraint" in str(err.orig).lower():
            raise HTTPException(status_code=400, detail="Invalid foreign key value")
        raise HTTPException(status_code=400, detail="Database constraint error")

    except KeyError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid field: {str(err)}")

    return MovieBaseDto.model_validate(movie)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie by ID.
    """
    movie = try_get_movie(movie_id, db)

    try:
        db.delete(movie)
        db.commit()
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

    return {"detail": f"Movie with ID {movie_id} has been deleted"}