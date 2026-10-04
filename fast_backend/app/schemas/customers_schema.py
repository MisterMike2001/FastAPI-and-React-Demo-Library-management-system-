from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    customer_first_name: str
    customer_surname: str
    customer_email: EmailStr
    customer_cell: str | None = None


class CustomerUpdate(BaseModel):
    customer_first_name: str | None = None
    customer_surname: str | None = None
    customer_email: EmailStr | None = None
    customer_cell: str | None = None