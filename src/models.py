from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.orm import DeclarativeBase, Relationship


class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    runtime = Column(Integer)
    imdb_id = Column(Integer)

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
