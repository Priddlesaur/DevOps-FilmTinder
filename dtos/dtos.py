from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class GenreDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = Field(None, read_only=True)
    username: str
    first_name: str
    last_name: str

