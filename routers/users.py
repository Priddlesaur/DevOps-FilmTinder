from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import UserDto, UserBaseDto
from models.base import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def try_get_user(user_id: int, db: Session) -> User:
    """
    Helper function for retrieving an existing user by ID or throwing a 404-error.
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserDto])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        HTTPException(status_code=404, detail="No users found")

    user_dtos = []
    for user in users:
        user_dtos.append(UserDto.model_validate(user))

    return user_dtos

@router.get("/{user_id}", response_model=UserDto)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user
    return UserDto.model_validate(user)

@router.post("/")
async def create_user(user: UserBaseDto, response: Response, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    new_user = User(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

    response.headers["Location"] = f"/ratings/{new_user.id}"

    return UserDto.model_validate(new_user)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with {user_id} has been deleted"}

@router.patch("/{user_id}", response_model=UserDto)
async def update_user(user_id: int, updated_user: UserBaseDto, db: Session = Depends(get_db)):
    """
    Update an existing user by ID.
    """
    user = try_get_user(user_id, db)

    updates = updated_user.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields for update")

    # Update the genre based on provided fields
    for key, value in updates.items():
        setattr(user, key, value)

    # Commit changes and handle potential errors
    db.commit()
    db.refresh(user)

    # Return the updated genre
    return UserDto.model_validate(user)
