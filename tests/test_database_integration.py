import database
from database import get_db
from main import app
from datetime import datetime
from sqlalchemy.orm import Session
from models.base import Base, Movie, Genre, User, Rating
from fastapi.testclient import TestClient

client = TestClient(app)


def fill_db(db: Session):
    drop_tables()
    create_tables()

    # Add test genre.
    genre = Genre(name="Comedy") # Genre id will be 1
    db.add(genre)
    db.commit()
    db.refresh(genre)

    # Add test movies.
    test_movies = [
        Movie(title="Gladiator", release_date=datetime(2024, 1, 1), runtime=180, imdb_id="tt1234567",
              genre_id=genre.id),
        Movie(title="The Dark Knight", release_date=datetime(2024, 1, 1), runtime=120, imdb_id="tt36223",
              genre_id=genre.id)
    ]
    for movie in test_movies:
        db.add(movie)
        db.commit()
        db.refresh(movie)

    # Add test users.
    test_users = [
        User(username="user1", first_name="John", last_name="Doe"),
        User(username="user2", first_name="Jane", last_name="Doe"),
        User(username="user3", first_name="Bob", last_name="Smith")
    ]
    for user in test_users:
        db.add(user)
        db.commit()
        db.refresh(user)

    # Add test ratings.
    test_ratings = [
        Rating(user_id=1, movie_id=2, rating=4, date=datetime(2024, 2, 10)),
        Rating(user_id=2, movie_id=1, rating=5, date=datetime(2024, 2, 10)),
        Rating(user_id=2, movie_id=2, rating=2, date=datetime(2024, 2, 10)),
        Rating(user_id=3, movie_id=2, rating=3, date=datetime(2024, 2, 10)),
        Rating(user_id=3, movie_id=1, rating=1, date=datetime(2024, 2, 10))
    ]
    for rating in test_ratings:
        db.add(rating)
        db.commit()
        db.refresh(rating)

def drop_tables():
    Base.metadata.drop_all(database.engine)

def create_tables():
    Base.metadata.create_all(database.engine)


def test_get_movie(db = next(get_db())):
    fill_db(db)

    response = client.get("/movies/1")

    assert response.status_code == 200
    movie = response.json()
    assert movie["title"] == "Gladiator"
    assert movie["runtime"] == 180
    assert movie["imdb_id"] == "tt1234567"

    drop_tables()

def test_get_movies(db = next(get_db())):
    fill_db(db)

    response = client.get("/movies")

    assert response.status_code == 200
    movies = response.json()
    assert len(movies) == 2
    assert movies[0]["title"] == "Gladiator"
    assert movies[0]["runtime"] == 180
    assert movies[0]["imdb_id"] == "tt1234567"
    assert movies[1]["title"] == "The Dark Knight"
    assert movies[1]["runtime"] == 120
    assert movies[1]["imdb_id"] == "tt36223"

    drop_tables()

def test_create_movie(db = next(get_db())):
    create_tables()

    genre = Genre(name = "Horror")
    db.add(genre)
    db.commit()

    movie_data = {
        "title": "Gladiator",
        "release_date": "2024-01-01",
        "runtime": 180,
        "imdb_id": "tt1234567",
        "genre_id": genre.id,
    }
    response = client.post("/movies/", json=movie_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Gladiator"
    assert data["runtime"] == 180

    drop_tables()

def test_upgrade_movie(db = next(get_db())):
    fill_db(db)

    updated_movie = {
        "title": "Gladiator II",
        "release_date": "2024-01-01",
        "runtime": 120
    }

    response = client.patch("/movies/1", json=updated_movie)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Gladiator II"
    assert data["runtime"] == 120
    assert data["imdb_id"] == "tt1234567"

    drop_tables()

def test_delete_movie(db = next(get_db())):
    fill_db(db)

    response = client.delete("/movies/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "Movie with ID 1 has been deleted"}

    drop_tables()

def test_get_user_recommendations(db = next(get_db())):
    fill_db(db)

    response = client.get("/users/1/recommend")
    assert response.status_code == 200
    assert response.json() == ['Gladiator']

    drop_tables()







