from fastapi import HTTPException
from tests.test_database_integration import fill_db, drop_tables, create_tables
import pytest
from database import get_db
from helpers.database_helpers import get_entity, create_or_rollback, update_or_rollback, delete_or_rollback
from datetime import datetime
from sqlalchemy import text
from models.base import Movie, Genre

def activate_foreign_key(db=next(get_db())):
    db.execute(text('PRAGMA foreign_keys = ON'))
    db.commit()

def create_genre(db=next(get_db())):
    genre = Genre(name="Horror")
    db.add(genre)
    db.commit()

def create_movie(db=next(get_db())):
    movie = Movie(title="Gladiator", release_date=datetime(2024, 1, 1), runtime=180, imdb_id="aay252434",
              genre_id=1)
    db.add(movie)
    db.commit()
    return movie

def fill_movie(runtime, imdb_id, genre_id):
    return {
        "title": "Gladiator",
        "release_date": datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        "runtime": runtime,
        "imdb_id": imdb_id,
        "genre_id": genre_id
    }

def fill_upgrade(runtime, imdb_id, genre_id):
    return {
        "title": "Gladiators",
        "runtime": runtime,
        "imdb_id": imdb_id,
        "genre_id": genre_id
    }



def test_get_entity_exception(db = next(get_db())):
    fill_db(db)

    # Should give an exception. The database is filled with 2 movies, therefore entity_id 3 does not exist.
    with pytest.raises(HTTPException) as exc_info:
        get_entity(Movie, 3, db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Entity not found"

    drop_tables()

def test_create_entity_foreign_key_exception(db=next(get_db())):
    activate_foreign_key(db)
    fill_db(db)

    # Should give an exception. The database is filled with 1 genre, therefore genre_id 2 does not exist.
    movie_data = fill_movie(180, "aay27502", 2)

    with pytest.raises(HTTPException) as e:
        create_or_rollback(Movie, movie_data, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Invalid foreign key value"

    drop_tables()

def test_create_entity_db_constraint_exception(db=next(get_db())):
    fill_db(db)

    # Should give an exception bc this imdb_id already exists in the database (via fill_db)
    movie_data = fill_movie(180, "tt1234567", 1)

    with pytest.raises(HTTPException) as e:
        create_or_rollback(Movie, movie_data, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Database constraint error"

    drop_tables()

def test_create_entity_type_exception(db=next(get_db())):
    fill_db(db)

    # Should give an exception, runtime is of type string but should be int
    movie_data = fill_movie("string", "aay27502", 1)

    with pytest.raises(HTTPException) as e:
        create_or_rollback(Movie, movie_data, db)

    assert e.value.status_code == 400
    assert "Invalid type input" in e.value.detail
    drop_tables()

def test_update_entity_foreign_key_exception(db = next(get_db())):
    activate_foreign_key(db)
    create_tables()
    create_genre(db)

    existing_movie = create_movie(db)

    # Should give an exception. The database is filled with 1 genre, therefore genre_id 2 does not exist.
    updated_movie = fill_upgrade(130, "tt1234567", 4)

    with pytest.raises(HTTPException) as e:
        update_or_rollback(existing_movie, updated_movie, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Invalid foreign key value"

    drop_tables()

def test_update_entity_db_constraint_exception(db = next(get_db())):
    fill_db(db)

    existing_movie = create_movie(db)

    # Should give an exception bc this imdb_id already exists in the database (via fill_db)
    updated_movie = fill_upgrade(130, "tt1234567", 1)

    with pytest.raises(HTTPException) as e:
        update_or_rollback(existing_movie, updated_movie, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Database constraint error"

    drop_tables()

def test_update_entity_input_exception(db = next(get_db())):
    create_tables()
    create_genre(db)

    existing_movie = create_movie(db)

    # Should give an exception, runtime is of type string but should be int
    updated_movie = fill_upgrade("string", "tt1234567", 1)

    with pytest.raises(HTTPException) as e:
        update_or_rollback(existing_movie, updated_movie, db)

    assert e.value.status_code == 400
    assert "Invalid type input" in e.value.detail

    drop_tables()

def test_update_entity_no_updates_exception(db = next(get_db())):
    create_tables()
    create_genre(db)

    existing_movie = create_movie(db)

    # Should give an exception bc the updated movie had no fields
    updated_movie = {}

    with pytest.raises(HTTPException) as e:
        update_or_rollback(existing_movie, updated_movie, db)

    assert e.value.status_code == 400
    assert e.value.detail == "No valid fields for update"

    drop_tables()

def test_delete_entity_exception(db = next(get_db())):
    create_tables()

    # Should give an exception bc the movie is of NoneType
    existing_movie1 = None

    with pytest.raises(HTTPException) as e:
        delete_or_rollback(existing_movie1, db)

    assert e.value.status_code == 400
    assert e.value.detail == "An error occurred while deleting"

    drop_tables()

