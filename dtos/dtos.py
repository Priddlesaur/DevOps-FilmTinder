from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class UserBaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(min_length=1, max_length=255, description="Username")
    first_name: str = Field(min_length=1, max_length=255, description="First Name")
    last_name: str = Field(min_length=1, max_length=255, description="Last Name")

class UserDto(UserBaseDto):
    model_config = ConfigDict(from_attributes=True)

    id: int = None

class GenreBaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=1, max_length=50, description="Name of the genre")

class GenreDto(GenreBaseDto):
    model_config = ConfigDict(from_attributes=True)

    id: int = None

class MovieBaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = Field(min_length=1, max_length=255, description="Title of the movie")
    release_date: Optional[datetime] = None
    runtime: Optional[int] = Field(min_length=1, description="Runtime of the movie")
    imdb_id: Optional[int] = Field(min_length=1, description="IMDB_ID")
    genre_id: Optional[int] = Field(min_length=1, description="Genre_ID")

class MovieDto(MovieBaseDto):
    model_config = ConfigDict(from_attributes=True)

    id: int = None

class RatingBaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movie_id: Optional[int] = None
    user_id: Optional[int] = None
    rating: Optional[int] = None
    date: Optional[datetime] = None

class RatingDto(RatingBaseDto):
    model_config = ConfigDict(from_attributes=True)

    id: int = None