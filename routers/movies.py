from fastapi import APIRouter, HTTPException
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

@router.get("/", response_model=list[MovieDto])
async def read_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")

    return [MovieDto.model_validate(movie) for movie in movies]

@router.get("/{movie_id}", response_model=MovieDto)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return MovieDto.model_validate(movie)

@router.post("/", response_model=MovieDto)
async def create_movie(movie: MovieDto, db: Session = Depends(get_db)):
    new_movie = Movie(**movie.model_dump())

    try:
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

    except IntegrityError as err:
        db.rollback()

        if "foreign key constraint" in str(err.orig).lower():
            raise HTTPException(status_code=400, detail="Invalid foreign key value")
        else:
            raise HTTPException(status_code=400, detail="Database constraint error")

    except KeyError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid field: {str(err)}")

    return MovieDto.model_validate(new_movie)

@router.patch("/{movie_id}", response_model=MovieBaseDto)
async def update_movie(movie_id: int, updated_movie: MovieBaseDto, db: Session = Depends(get_db)):
    # Zoek de film in de database
    movie = db.query(Movie).filter_by(id=movie_id).first()

    # Controleer of de film bestaat
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Update alleen de velden die in de patch-aanvraag zijn gespecificeerd
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
        else:
            raise HTTPException(status_code=400, detail="Database constraint error")

    except KeyError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid field: {str(err)}")

    # Retourneer de bijgewerkte film
    return MovieBaseDto.model_validate(movie)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()

    return {"detail": f"Movie with ID {movie_id} has been deleted"}