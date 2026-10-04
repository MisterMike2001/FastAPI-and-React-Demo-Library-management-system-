from datetime import date

from pydantic import BaseModel


class BookLoanCreate(BaseModel):
    customer_id: int
    inventory_id: int
    date_loaned: date
    date_due: date
    date_returned: date | None = None


class BookLoanUpdate(BaseModel):
    customer_id: int | None = None
    inventory_id: int | None = None
    date_loaned: date | None = None
    date_due: date | None = None
    date_returned: date | None = None