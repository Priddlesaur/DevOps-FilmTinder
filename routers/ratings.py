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

@router.get("/", response_model=list[RatingDto])
async def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).all()
    if not ratings:
        HTTPException(status_code=404, detail="No ratings found")

    rating_dtos = []
    for rating in ratings:
        rating_dtos.append(RatingDto.model_validate(rating))

    return rating_dtos

@router.get("/{id}", response_model=RatingDto)
async def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).get(rating_id)
    if not rating:
        HTTPException(status_code=404, detail="Rating not found")

    return RatingDto.model_validate(rating)

@router.post("/", status_code=201, response_model=RatingDto)
async def create_rating(rating: RatingBaseDto, response: Response, db: Session = Depends(get_db)):
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

@router.patch("/{id}", response_model=RatingDto)
async def update_rating(rating_id: int, updated_rating: RatingBaseDto, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter_by(id=rating_id).first()
    if not rating:
        HTTPException(status_code=404, detail="Rating not found")

    for key, value in updated_rating.model_dump(exclude_none=True).items():
        setattr(rating, key, value)

    db.commit()

    return RatingDto.model_validate(rating)

@router.delete("/{id}", response_model=RatingDto)
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter_by(id=rating_id).first()
    if not rating:
        HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating)
    db.commit()

    return {"message": f"Rating with {rating_id} has been deleted"}