from sqlalchemy.orm import Session

from dtos.dtos import UserBaseDto
from models.base import User
from database import get_db
import random

def generate_test_users(count=100):
    """
    Generates a list of test users.
    """
    first_names = ["John", "Alice", "Bob", "Sarah", "Michael", "Emily", "Chris", "Jessica"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis"]

    users = []
    for i in range(count):
        username = f"user{i:03d}"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        users.append({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        })
    return users

def populate_users():
    """
    Populates the database with generated test users.
    """
    db: Session = next(get_db())

    # Check if users are already populated to avoid duplicates
    if db.query(User).count() > 0:
        print("Users already processed")
        return

    print("Generating test users...")
    test_users = generate_test_users(count=100)

    print("Processing users...")
    count_added = 0

    for user_data in test_users:
        user = UserBaseDto(**user_data)

        if try_add_user(user, db):
            count_added += 1

    print(f"Finished processing users. Total added: {count_added}")

def try_add_user(user, db):
    """
    Tries to add a user to the database.
    """
    try:
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        print(f"Added user {user.username}")
        return True
    except Exception as e:
        print(f"Failed to add user {user.username}: {e}")
        db.rollback()
        return False
