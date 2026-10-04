from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(100), nullable=False, unique=True)
    genre_descr = Column(String(255), nullable=False)

    books = relationship("Book", back_populates="genre")