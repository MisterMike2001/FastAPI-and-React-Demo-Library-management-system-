from sqlalchemy import Column, Integer, String

from app.models.base_model import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    user_first_name = Column(String(100), nullable=False)
    user_surname = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    user_cell = Column(String(20), nullable=True)