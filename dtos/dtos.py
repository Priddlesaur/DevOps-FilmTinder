from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GenreDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

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