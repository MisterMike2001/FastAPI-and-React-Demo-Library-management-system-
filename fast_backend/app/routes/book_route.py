from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.repositories.books_repo import BookRepo
from app.models.books_model import Book

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/")
def get_books(db: Session = Depends(get_db)):
    book_repo = BookRepo(db)
    books = book_repo.get_all_books()

    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    
    return books


@router.get("/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_repo = BookRepo(db)
    book = book_repo.get_book_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@router.put("/update/{book_id}")
def update_book(
    book_id: int,
    book_name: str | None = None,
    book_descr: str | None = None,
    book_isbn: str | None = None,
    book_author_id: int | None = None,
    book_genre_id: int | None = None,
    db: Session = Depends(get_db),
):
    book_repo = BookRepo(db)

    changes = Book(
        book_name=book_name,
        book_descr=book_descr,
        book_isbn=book_isbn,
        book_author_id=book_author_id,
        book_genre_id=book_genre_id,
    )

    updated_book = book_repo.update_book(book_id, changes)

    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated_book


@router.post("/create/", status_code=201)
def create_book(
    book_name: str,
    book_descr: str,
    book_author_id: int,
    book_genre_id: int,
    book_isbn: str | None = None,
    db: Session = Depends(get_db),
):
    book_repo = BookRepo(db)

    book = Book(
        book_name=book_name,
        book_descr=book_descr,
        book_isbn=book_isbn,
        book_author_id=book_author_id,
        book_genre_id=book_genre_id,
    )

    return book_repo.create_book(book)


@router.delete("/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepo(db)
    item = repo.delete_book(book_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
