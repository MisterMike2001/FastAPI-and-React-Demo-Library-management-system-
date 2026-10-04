from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class BookInventory(Base):
    __tablename__ = "book_inventory"

    inventory_id = Column(Integer, primary_key=True)

    book_id = Column(
        Integer,
        ForeignKey("books.book_id"),
        nullable=False,
    )

    inventory_status_id = Column(
        Integer,
        ForeignKey("inventory_status.inventory_status_id"),
        nullable=False,
    )

    book = relationship("Book", back_populates="inventory")
    status = relationship(
        "InventoryStatus",
        back_populates="inventory_items",
    )
    loans = relationship("BookLoan", back_populates="inventory")