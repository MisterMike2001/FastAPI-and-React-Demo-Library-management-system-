from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    book_name = Column(String(100), nullable=False)
    book_descr = Column(String(255), nullable=False)
    book_isbn = Column(String(20), nullable=True, unique=True)

    book_genre_id = Column(
        Integer,
        ForeignKey("genres.genre_id"),
        nullable=False,
    )

    book_author_id = Column(
        Integer,
        ForeignKey("authors.author_id"),
        nullable=False,
    )

    genre = relationship("Genre", back_populates="books")
    author = relationship("Author", back_populates="books")
    inventory = relationship("BookInventory", back_populates="book")