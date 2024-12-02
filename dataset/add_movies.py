import os

import kagglehub
from sqlalchemy.orm import Session

from dtos.dtos import MovieBaseDto, GenreBaseDto
from datetime import datetime
from database import get_db
from models.base import Genre, Movie

MAX_MOVIES = 50_000
COLUMN_NAMES = [
    "id", "title", "vote_average", "vote_count", "status", "release_date", "revenue", "runtime", "adult",
    "backdrop_path", "budget", "homepage", "imdb_id", "original_language", "original_title", "overview",
    "popularity", "poster_path", "tagline", "genres", "production_companies", "production_countries",
    "spoken_languages", "keywords",
]

def populate_database():
    """
    Populates the database with movies from the TMDB dataset.
    :return: None
    """

    db: Session = next(get_db())

    # Check if dataset has already been processed, because it takes a long time
    # and we don't want to do it every time the server starts.
    if db.query(Movie).count() > 0:
        print("Dataset already processed")
        return

    print("Fetching dataset...")
    dataset_path = kagglehub.dataset_download("asaniczka/tmdb-movies-dataset-2023-930k-movies")
    csv_file_name = os.listdir(dataset_path)[0]
    if not csv_file_name.endswith(".csv"):
        print("Invalid dataset file")
        return

    print("Opening dataset file...")
    file = open(f"{dataset_path}/{csv_file_name}", "r", encoding="utf-8")
    lines = file.readlines()
    file.close()

    title_index = COLUMN_NAMES.index("title")
    release_date_index = COLUMN_NAMES.index("release_date")
    runtime_index = COLUMN_NAMES.index("runtime")
    imdb_id_index = COLUMN_NAMES.index("imdb_id")
    genres_index = COLUMN_NAMES.index("genres")

    print("Processing movies...")
    count_added = 0

    for index, line in enumerate(lines):
        if index == 0:
            continue

        if count_added >= MAX_MOVIES:
            break

        columns = split_csv_line(line)
        movie_title = columns[title_index]
        movie_release_date = columns[release_date_index]
        movie_runtime = int(columns[runtime_index])
        movie_imdb_id = columns[imdb_id_index]
        if len(movie_title) > 100:
            print(f"Skipping movie {movie_title} because it has a title longer than 100 characters")
            continue
        if len(movie_release_date) != 10:
            print(f"Skipping movie {movie_title} because it has an invalid release date")
            continue
        if movie_runtime < 1:
            print(f"Skipping movie {movie_title} because it has no runtime")
            continue
        if movie_imdb_id == "":
            print(f"Skipping movie {movie_title} because it has no IMDB ID")
            continue

        genres_str = columns[genres_index]
        genres_data = genres_str.split(",")
        genres_data = [genre.strip() for genre in genres_data]
        genre_name = genres_data[0]
        if genre_name == "":
            print(f"Skipping movie {movie_title} because it has no genre")
            continue

        genre_id = None
        if len(genres_data) > 0:
            genre_id = get_or_create_genre_id(genre_name, db)

        print(f"Processing movie {count_added}/{MAX_MOVIES} ({(count_added / MAX_MOVIES) * 100:.2f}%)")

        movie = MovieBaseDto(
            title=movie_title,
            release_date=datetime.strptime(movie_release_date, "%Y-%m-%d"),
            runtime=movie_runtime,
            imdb_id=movie_imdb_id,
            genre_id=genre_id,
        )

        if try_add_movie(movie, db):
            count_added += 1

    print("Finished processing movies")

def try_add_movie(movie, db):
    """
    Tries to add a movie to the database.
    :param movie: The movie to add.
    :param db: The database session.
    :return: True if the movie was added successfully, False otherwise.
    """
    try:
        new_movie = Movie(**movie.model_dump())
        db.add(new_movie)
        db.commit()
        return True
    except Exception as e:
        print(f"Failed to add movie {movie.title} to the database: {e}")
        db.rollback()
        return False

def get_or_create_genre_id(genre_name: str, db: Session):
    """
    Gets the ID of a genre from the database, or creates a new genre if it doesn't exist.
    :param genre_name: The name of the genre.
    :param db: The database session.
    :return: The ID of the genre.
    """
    genre = db.query(Genre).filter(Genre.name == genre_name).first()
    if genre:
        return genre.id

    # Create new genre
    new_genre = Genre(**GenreBaseDto(name=genre_name).model_dump())
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)

    # Return genre ID
    return new_genre.id

def split_csv_line(line):
    """
    Splits a CSV line into columns.
    :param line: The line to split.
    :return: A list of columns.
    """
    data = []
    column = ""
    in_quotes = False
    for char in line:
        if char == "," and not in_quotes:
            data.append(column)
            column = ""
        elif char == "\"":
            in_quotes = not in_quotes
        else:
            column += char

    return data
