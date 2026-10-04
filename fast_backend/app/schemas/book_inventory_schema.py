from pydantic import BaseModel


class BookInventoryCreate(BaseModel):
    book_id: int
    inventory_status_id: int


class BookInventoryUpdate(BaseModel):
    book_id: int | None = None
    inventory_status_id: int | None = None