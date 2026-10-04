from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True)
    author_first_name = Column(String(100), nullable=False)
    author_surname = Column(String(100), nullable=False)


    books = relationship("Book", back_populates="author")