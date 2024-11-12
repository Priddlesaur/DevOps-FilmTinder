from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    runtime = Column(Integer)
    imdb_id = Column(Integer)