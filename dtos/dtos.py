from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GenreBaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=1, max_length=50, description="Name of the genre")

class GenreDto(GenreBaseDto):
    model_config = ConfigDict(from_attributes=True)

    id: int = None

class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    username: str
    first_name: str
    last_name: str

class MovieDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = None
    title: str
    release_date: datetime
    runtime: int
    imdb_id: int
    genre_id: int

class MovieUpdateDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    release_date: Optional[datetime] = None
    runtime: Optional[int] = None
    imdb_id: Optional[int] = None
    genre_id: Optional[int] = None
