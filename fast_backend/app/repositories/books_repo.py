

from app.models.books_model import Book


class BookRepo:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_book_by_id(self, book_id: int):
        return self.db_session.query(Book).filter(Book.book_id == book_id).first()

    def get_all_books(self):
        return self.db_session.query(Book).all()

    def create_book(self, book: Book):
        self.db_session.add(book)
        self.db_session.commit()
        self.db_session.refresh(book)
        return book

    def update_book(self, book_id: int, updated_book: Book):
        book = self.get_book_by_id(book_id)
        if book is None:
            return None

        if updated_book.book_name is not None:
            book.book_name = updated_book.book_name

        if updated_book.book_descr is not None:
            book.book_descr = updated_book.book_descr

        if updated_book.book_isbn is not None:
            book.book_isbn = updated_book.book_isbn

        if updated_book.book_author_id is not None:
            book.book_author_id = updated_book.book_author_id

        if updated_book.book_genre_id is not None:
            book.book_genre_id = updated_book.book_genre_id

        self.db_session.commit()
        self.db_session.refresh(book)
        return book

    def delete_book(self, book_id: int):
        item = self.get_book_by_id(book_id)
        if item is None:
            return None
        self.db_session.delete(item)
        self.db_session.commit()
        return item
