from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.models.inventory_status_model import InventoryStatus
from app.repositories.inventory_status_repo import InventoryStatusRepo

router = APIRouter(prefix="/inventory_status", tags=["inventory_status"])


@router.get("/")
def get_inventory_status(db: Session = Depends(get_db)):
    repo = InventoryStatusRepo(db)
    items = repo.get_all_inventory_status()
    if not items:
        raise HTTPException(status_code=404, detail="No inventory status found")
    return items


@router.get("/{inventory_status_id}")
def get_inventory_status_by_id(inventory_status_id: int, db: Session = Depends(get_db)):
    repo = InventoryStatusRepo(db)
    item = repo.get_inventory_status_by_id(inventory_status_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventorystatus not found")
    return item


@router.put("/update/{inventory_status_id}")
def update_inventory_status(
    inventory_status_id: int,
    inventory_status_name: str | None = None,
    inventory_status_descr: str | None = None,
    db: Session = Depends(get_db),
):
    repo = InventoryStatusRepo(db)
    changes = InventoryStatus(
        inventory_status_name=inventory_status_name,
        inventory_status_descr=inventory_status_descr,
    )
    item = repo.update_inventory_status(inventory_status_id, changes)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventorystatus not found")
    return item


@router.post("/create/", status_code=201)
def create_inventory_status(
    inventory_status_name: str,
    inventory_status_descr: str,
    db: Session = Depends(get_db),
):
    repo = InventoryStatusRepo(db)
    item = InventoryStatus(
        inventory_status_name=inventory_status_name,
        inventory_status_descr=inventory_status_descr,
    )
    return repo.create_inventory_status(item)


@router.delete("/delete/{inventory_status_id}")
def delete_inventory_status(inventory_status_id: int, db: Session = Depends(get_db)):
    repo = InventoryStatusRepo(db)
    item = repo.delete_inventory_status(inventory_status_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventorystatus not found")
    return {"message": "Inventorystatus deleted"}
