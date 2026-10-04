from pydantic import BaseModel


class InventoryStatusCreate(BaseModel):
    inventory_status_name: str
    inventory_status_descr: str


class InventoryStatusUpdate(BaseModel):
    inventory_status_name: str | None = None
    inventory_status_descr: str | None = None