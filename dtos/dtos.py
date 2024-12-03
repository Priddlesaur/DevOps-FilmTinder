from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserBaseDto(BaseDto):
    username: Optional[str] = Field(default=None, min_length=5, max_length=50, description="Username")
    first_name: Optional[str] = Field(default=None, min_length=5, max_length=50, description="First name")
    last_name: Optional[str] = Field(default=None, min_length=5, max_length=50, description="Last name")

class UserDto(UserBaseDto):
    id: Optional[int] = Field(default=None, description="Unique identifier for the user")

class GenreBaseDto(BaseDto):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50, description="Name of the genre")

class GenreDto(GenreBaseDto):
    id: Optional[int] = Field(default=None, description="Unique identifier for the genre")

class MovieBaseDto(BaseDto):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Title of the movie")
    release_date: Optional[datetime] = Field(default=None, description="Release date of the movie")
    runtime: Optional[int] = Field(default=None, ge=1, description="Runtime of the movie")
    imdb_id: Optional[str] = Field(default=None, max_length=10, description="IMDB ID of the movie")
    genre_id: Optional[int] = Field(default=None, description="Genre of the movie")

class MovieDto(MovieBaseDto):
    id: Optional[int] = Field(default=None, description="Unique identifier for the movie")

class RatingBaseDto(BaseDto):
    movie_id: Optional[int] = Field(default=None, description="Movie ID of rated movie")
    user_id: Optional[int] = Field(default=None, description="User ID of rating user")
    rating: Optional[int] = Field(default=None, ge=1, le=5, description="Rating for the movie (1-5)")
    date: Optional[datetime] = Field(default=None, description="Date of the rating")

class RatingDto(RatingBaseDto):
    id: Optional[int] = Field(default=None, description="Unique identifier for the rating")