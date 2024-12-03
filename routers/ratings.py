from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import RatingDto, RatingBaseDto
from helpers.database_helpers import delete_or_rollback, get_all_entities, get_entity, create_or_rollback, \
    update_or_rollback
from models.base import Rating

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
)

@router.get("/", response_model=list[RatingDto])
async def read_ratings(db: Session = Depends(get_db)):
    ratings = get_all_entities(Rating, db)
    return [RatingDto.model_validate(rating) for rating in ratings]

@router.get("/{rating_id}", response_model=RatingDto)
async def read_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = get_entity(Rating, rating_id, db)
    return RatingDto.model_validate(rating)

@router.post("/", status_code=201, response_model=RatingDto)
async def create_rating(rating: RatingBaseDto, response: Response, db: Session = Depends(get_db)):
    new_rating = create_or_rollback(Rating, rating.model_dump(), db)
    response.headers["Location"] = f"/ratings/{new_rating.id}"
    return RatingDto.model_validate(new_rating)

@router.patch("/{rating_id}", response_model=RatingDto)
async def update_rating(rating_id: int, updated_rating: RatingBaseDto, db: Session = Depends(get_db)):
    rating = get_entity(Rating, rating_id, db)
    updates = updated_rating.model_dump(exclude_none=True)
    updated_rating_final = update_or_rollback(rating, updates, db)
    return RatingDto.model_validate(updated_rating_final)

@router.delete("/{rating_id}", response_model=RatingDto)
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = get_entity(Rating, rating_id, db)
    delete_or_rollback(rating,db)
    return {"message": f"Rating with ID {rating_id} has been deleted"}