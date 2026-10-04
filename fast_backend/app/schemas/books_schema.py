from pydantic import BaseModel


class BookCreate(BaseModel):
    book_name: str
    book_descr: str
    book_isbn: str | None = None
    book_genre_id: int
    book_author_id: int


class BookUpdate(BaseModel):
    book_name: str | None = None
    book_descr: str | None = None
    book_isbn: str | None = None
    book_genre_id: int | None = None
    book_author_id: int | None = None