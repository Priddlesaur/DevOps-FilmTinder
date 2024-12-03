from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import UserDto, UserBaseDto
from helpers.database_helpers import delete_or_rollback, get_all_entities, get_entity, create_or_rollback, \
    update_or_rollback
from models.base import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=list[UserDto])
async def read_users(db: Session = Depends(get_db)):
    users = get_all_entities(User, db)
    return [UserDto.model_validate(user) for user in users]

@router.get("/{user_id}", response_model=UserDto)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_entity(User, user_id, db)
    return UserDto.model_validate(user)

@router.post("/")
async def create_user(user: UserBaseDto, response: Response, db: Session = Depends(get_db)):
    new_user = create_or_rollback(User, user.model_dump(), db)
    response.headers["Location"] = f"/ratings/{new_user.id}"
    return UserDto.model_validate(new_user)

@router.patch("/{user_id}", response_model=UserDto)
async def update_user(user_id: int, updated_user: UserBaseDto, db: Session = Depends(get_db)):
    user = get_entity(User, user_id, db)
    updates = updated_user.model_dump(exclude_none=True)
    updated_user_final = update_or_rollback(user, updates, db)
    return UserDto.model_validate(updated_user_final)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_entity(User,user_id, db)
    delete_or_rollback(user,db)
    return {"message": f"User with ID {user_id} has been deleted"}


