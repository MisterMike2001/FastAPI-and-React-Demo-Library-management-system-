from pydantic import BaseModel


class AuthorCreate(BaseModel):
    author_first_name: str
    author_surname: str


class AuthorUpdate(BaseModel):
    author_first_name: str | None = None
    author_surname: str | None = None