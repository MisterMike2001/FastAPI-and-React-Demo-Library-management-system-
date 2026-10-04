from pydantic import BaseModel


class GenreCreate(BaseModel):
    genre_name: str
    genre_descr: str


class GenreUpdate(BaseModel):
    genre_name: str | None = None
    genre_descr: str | None = None