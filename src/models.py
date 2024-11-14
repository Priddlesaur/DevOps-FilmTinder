from sqlalchemy import nullsfirst, Integer, Date, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
