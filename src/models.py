from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Relationship


class Base(DeclarativeBase):
    pass

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)














