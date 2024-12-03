from sqlalchemy.orm import Session
from datetime import date, timedelta
import random

from models.base import Rating, User, Movie
from database import get_db

def generate_random_ratings(user_ids, movie_ids, count=100):
    """
    Generates a list of random ratings for movies by users.
    """
    ratings = []
    generated_pairs = set()

    while len(ratings) < count:
        user_id = random.choice(user_ids)
        movie_id = random.choice(movie_ids)
        pair = (user_id, movie_id)

        if pair not in generated_pairs:
            rating_value = random.randint(1, 5)  # Assuming a rating scale from 1 to 5
            rating_date = date.today() - timedelta(days=random.randint(0, 365))  # Random date within the last year

            ratings.append({
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating_value,
                "date": rating_date
            })
            generated_pairs.add(pair)

    return ratings

def populate_ratings():
    """
    Populates the database with generated random ratings.
    """
    db: Session = next(get_db())

    # Check if ratings are already populated to avoid duplicates
    if db.query(Rating).count() > 0:
        print("Ratings already processed")
        return

    print("Fetching existing users and movies...")
    user_ids = [u.id for u in db.query(User).all()]
    movie_ids = [m.id for m in db.query(Movie).all()]

    if not user_ids or not movie_ids:
        print("No users or movies found in the database. Cannot generate ratings.")
        return

    print("Generating random ratings...")
    random_ratings = generate_random_ratings(user_ids, movie_ids, count=50000)

    print("Processing ratings...")
    count_added = 0

    for rating_data in random_ratings:
        if try_add_rating(rating_data, db):
            count_added += 1

    print(f"Finished processing ratings. Total added: {count_added}")

def try_add_rating(rating_data, db):
    """
    Tries to add a rating to the database.
    """
    try:
        new_rating = Rating(**rating_data)
        db.add(new_rating)
        db.commit()
        print(f"Added rating for movie {rating_data['movie_id']} by user {rating_data['user_id']}")
        return True
    except Exception as e:
        print(f"Failed to add rating: {e}")
        db.rollback()
        return False
