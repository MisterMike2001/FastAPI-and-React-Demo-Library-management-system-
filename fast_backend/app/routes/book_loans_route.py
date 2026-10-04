from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.models.book_loans_model import BookLoan
from app.repositories.book_loans_repo import BookLoanRepo

router = APIRouter(prefix="/book_loans", tags=["book_loans"])


@router.get("/")
def get_book_loans(db: Session = Depends(get_db)):
    repo = BookLoanRepo(db)
    items = repo.get_all_book_loans()
    if not items:
        raise HTTPException(status_code=404, detail="No book loans found")
    return items


@router.get("/{loan_id}")
def get_book_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    repo = BookLoanRepo(db)
    item = repo.get_book_loan_by_id(loan_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book loan not found")
    return item


@router.put("/update/{loan_id}")
def update_book_loan(
    loan_id: int,
    customer_id: int | None = None,
    inventory_id: int | None = None,
    date_loaned: date | None = None,
    date_due: date | None = None,
    date_returned: date | None = None,
    db: Session = Depends(get_db),
):
    repo = BookLoanRepo(db)
    changes = BookLoan(
        customer_id=customer_id,
        inventory_id=inventory_id,
        date_loaned=date_loaned,
        date_due=date_due,
        date_returned=date_returned,
    )
    item = repo.update_book_loan(loan_id, changes)
    if item is None:
        raise HTTPException(status_code=404, detail="Book loan not found")
    return item


@router.post("/create/", status_code=201)
def create_book_loan(
    customer_id: int,
    inventory_id: int,
    date_loaned: date,
    date_due: date,
    date_returned: date | None = None,
    db: Session = Depends(get_db),
):
    repo = BookLoanRepo(db)
    item = BookLoan(
        customer_id=customer_id,
        inventory_id=inventory_id,
        date_loaned=date_loaned,
        date_due=date_due,
        date_returned=date_returned,
    )
    return repo.create_book_loan(item)


@router.delete("/delete/{loan_id}")
def delete_book_loan(loan_id: int, db: Session = Depends(get_db)):
    repo = BookLoanRepo(db)
    item = repo.delete_book_loan(loan_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book loan not found")
    return {"message": "Book loan deleted"}
