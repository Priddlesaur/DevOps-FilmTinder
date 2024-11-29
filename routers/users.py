from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dtos.dtos import UserDto, UserBaseDto
from models.base import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=list[UserDto])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        HTTPException(status_code=404, detail="No users found")

    user_dtos = []
    for user in users:
        user_dtos.append(UserDto.model_validate(user))

    return user_dtos

# @router.get("/")
# async def read_users(username: str | None = None,
#                      first_name: str | None = None,
#                      last_name: str | None = None,
#                      db: Session = Depends(get_db)):
#     # Receiving a user by username if there is a username given in the URL
#     if username:
#         user = db.query(User).filter(User.username == username).first()
#         # If there is not a user with the given username, give an error
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         # else return the user
#         return UserDto.model_validate(user)
#     if first_name and last_name:
#         user = db.query(User).filter(User.first_name == first_name, User.last_name == last_name).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return UserDto.model_validate(user)
#     elif first_name:
#         user = db.query(User).filter(User.first_name == first_name).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return UserDto.model_validate(user)
#     elif last_name:
#         user = db.query(User).filter(User.last_name == last_name).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return UserDto.model_validate(user)
#     else:
#         # If there is no username given in the URL, get all users
#         users = db.query(User).all()
#         # If there are no users, give an error
#         if not users:
#             raise HTTPException(status_code=404, detail="No users found")
#
#         # For every user in users, put them in a list
#         user_dtos = []
#         for user in users:
#             user_dtos.append(UserDto.model_validate(user))
#
#         # Return the users
#         return user_dtos

@router.get("/{user_id}", response_model=UserDto)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user
    return UserDto.model_validate(user)

@router.post("/")
async def create_user(user: UserDto, db: Session = Depends(get_db)):
    # Check if username is unique
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"User added successfully": new_user}

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with {user_id} has been deleted"}

@router.delete("/")
async def delete_user(username : str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"User with deleted"}

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserDto, db: Session = Depends(get_db)):
    # Receiving the user with the filled in user_id
    db_user = db.query(User).get(user_id)
    # If user does not exist give an error
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Renewing the changes
    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db.commit()
    db.refresh(db_user)
    return {"User updated successfully": db_user}

@router.put("/")
async def update_user(username : str, user: UserDto, db: Session = Depends(get_db)):
    # Receiving the user with the given username
    db_user = db.query(User).filter(User.username == username).first()
    # If the user does not exist give an error
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    #Renewing the changes
    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db.commit()
    db.refresh(db_user)
    return {"User updated successfully": db_user}




