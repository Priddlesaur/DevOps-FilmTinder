from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import RatingDto, RatingBaseDto
from models.base import Rating

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
)

def try_get_rating(rating_id: int, db: Session) -> Rating:
    """
    Helper function for retrieving an existing rating by ID or throwing a 404-error.
    """
    rating = db.query(Rating).get(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.get("/", response_model=list[RatingDto])
async def read_ratings(db: Session = Depends(get_db)):
    """
    Retrieve all ratings.
    """
    ratings = db.query(Rating).all()
    if not ratings:
        HTTPException(status_code=404, detail="No ratings found")

    rating_dtos = []
    for rating in ratings:
        rating_dtos.append(RatingDto.model_validate(rating))

    return rating_dtos

@router.get("/{rating_id}", response_model=RatingDto)
async def read_rating(rating_id: int, db: Session = Depends(get_db)):
    """
    Retrieve rating by ID.
    """
    rating = try_get_rating(rating_id, db)

    return RatingDto.model_validate(rating)

@router.post("/", status_code=201, response_model=RatingDto)
async def create_rating(rating: RatingBaseDto, response: Response, db: Session = Depends(get_db)):
    """
    Create a new rating.
    """
    new_rating = Rating(**rating.model_dump())

    try:
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

    response.status_code = 201
    response.headers["Location"] = f"/ratings/{new_rating.id}"

    return RatingDto.model_validate(new_rating)

@router.patch("/{rating_id}", response_model=RatingDto)
async def update_rating(rating_id: int, updated_rating: RatingBaseDto, db: Session = Depends(get_db)):
    """
    Update an existing rating by ID.
    """
    rating = try_get_rating(rating_id, db)

    for key, value in updated_rating.model_dump(exclude_none=True).items():
        setattr(rating, key, value)

    db.commit()
    db.refresh(rating)

    return RatingDto.model_validate(rating)

@router.delete("/{rating_id}", response_model=RatingDto)
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing rating by ID.
    """
    rating = try_get_rating(rating_id, db)

    db.delete(rating)
    db.commit()

    return {"message": f"Rating with {rating_id} has been deleted"}