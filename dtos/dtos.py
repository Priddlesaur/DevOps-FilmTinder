from pydantic import BaseModel, ConfigDict


class GenreDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
