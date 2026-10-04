from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.models.customers_model import Customer
from app.repositories.customer_repo import CustomerRepo

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    repo = CustomerRepo(db)
    items = repo.get_all_customers()
    if not items:
        raise HTTPException(status_code=404, detail="No customers found")
    return items


@router.get("/{customer_id}")
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    repo = CustomerRepo(db)
    item = repo.get_customer_by_id(customer_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return item


@router.put("/update/{customer_id}")
def update_customer(
    customer_id: int,
    customer_first_name: str | None = None,
    customer_surname: str | None = None,
    customer_email: str | None = None,
    customer_cell: str | None = None,
    db: Session = Depends(get_db),
):
    repo = CustomerRepo(db)
    changes = Customer(
        customer_first_name=customer_first_name,
        customer_surname=customer_surname,
        customer_email=customer_email,
        customer_cell=customer_cell,
    )
    item = repo.update_customer(customer_id, changes)
    if item is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return item


@router.post("/create/", status_code=201)
def create_customer(
    customer_first_name: str,
    customer_surname: str,
    customer_email: str,
    customer_cell: str | None = None,
    db: Session = Depends(get_db),
):
    repo = CustomerRepo(db)
    item = Customer(
        customer_first_name=customer_first_name,
        customer_surname=customer_surname,
        customer_email=customer_email,
        customer_cell=customer_cell,
    )
    return repo.create_customer(item)


@router.delete("/delete/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    repo = CustomerRepo(db)
    item = repo.delete_customer(customer_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}
