from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GenreDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class MovieDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    release_date: datetime
    runtime: int
    imdb_id: int
    genre_id: int