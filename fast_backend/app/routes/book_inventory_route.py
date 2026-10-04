from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.models.book_inventory_model import BookInventory
from app.repositories.book_inventory_repo import BookInventoryRepo

router = APIRouter(prefix="/book_inventory", tags=["book_inventory"])


@router.get("/")
def get_book_inventory(db: Session = Depends(get_db)):
    repo = BookInventoryRepo(db)
    items = repo.get_all_book_inventory()
    if not items:
        raise HTTPException(status_code=404, detail="No book inventory found")
    return items


@router.get("/{inventory_id}")
def get_book_inventory_by_id(inventory_id: int, db: Session = Depends(get_db)):
    repo = BookInventoryRepo(db)
    item = repo.get_book_inventory_by_id(inventory_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book inventory not found")
    return item


@router.put("/update/{inventory_id}")
def update_book_inventory(
    inventory_id: int,
    book_id: int | None = None,
    inventory_status_id: int | None = None,
    db: Session = Depends(get_db),
):
    repo = BookInventoryRepo(db)
    changes = BookInventory(
        book_id=book_id,
        inventory_status_id=inventory_status_id,
    )
    item = repo.update_book_inventory(inventory_id, changes)
    if item is None:
        raise HTTPException(status_code=404, detail="Book inventory not found")
    return item


@router.post("/create/", status_code=201)
def create_book_inventory(
    book_id: int,
    inventory_status_id: int,
    db: Session = Depends(get_db),
):
    repo = BookInventoryRepo(db)
    item = BookInventory(
        book_id=book_id,
        inventory_status_id=inventory_status_id,
    )
    return repo.create_book_inventory(item)


@router.delete("/delete/{inventory_id}")
def delete_book_inventory(inventory_id: int, db: Session = Depends(get_db)):
    repo = BookInventoryRepo(db)
    item = repo.delete_book_inventory(inventory_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book inventory not found")
    return {"message": "Book inventory deleted"}
