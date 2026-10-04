from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class InventoryStatus(Base):
    __tablename__ = "inventory_status"

    inventory_status_id = Column(Integer, primary_key=True)
    inventory_status_name = Column(
        String(100),
        nullable=False,
        unique=True,
    )
    inventory_status_descr = Column(String(255), nullable=False)

    inventory_items = relationship(
        "BookInventory",
        back_populates="status",
    )