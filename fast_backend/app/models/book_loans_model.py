from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class BookLoan(Base):
    __tablename__ = "book_loans"

    loan_id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    inventory_id = Column(
        Integer,
        ForeignKey("book_inventory.inventory_id"),
        nullable=False,
    )

    date_loaned = Column(Date, nullable=False)
    date_due = Column(Date, nullable=False)
    date_returned = Column(Date, nullable=True)

    customer = relationship("Customer", back_populates="loans")
    inventory = relationship("BookInventory", back_populates="loans")