from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    customer_first_name = Column(String(100), nullable=False)
    customer_surname = Column(String(100), nullable=False)
    customer_email = Column(String(255), nullable=False, unique=True)
    customer_cell = Column(String(20), nullable=True)

    loans = relationship("BookLoan", back_populates="customer")