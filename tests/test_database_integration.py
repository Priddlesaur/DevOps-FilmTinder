import os
import pytest
import database
from database import get_db
from main import app
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.base import Base, Movie, Genre
from fastapi.testclient import TestClient

client = TestClient(app)

def fill_db(db: Session):
    Base.metadata.create_all(database.engine)

    genre = Genre(name="Comedy")
    db.add(genre)
    db.commit()

    movie_data = [
        Movie(title="Gladiator", release_date=datetime(2024, 1, 1), runtime=180, imdb_id="tt1234567",
              genre_id=genre.id),
        Movie(title="The Dark Knight", release_date=datetime(2024, 1, 1), runtime=120, imdb_id="tt36223",
              genre_id=genre.id)
    ]

    for movie in movie_data:
        db.add(movie)
        db.commit()

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
    assert response.json() == {"detail": f"Movie with ID 1 has been deleted"}

    drop_tables()














