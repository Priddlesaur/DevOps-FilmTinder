from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Date, ForeignKey

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    release_date = Column(Date)
    runtime = Column(Integer)
    imdb_id = Column(Integer, unique=True)

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

