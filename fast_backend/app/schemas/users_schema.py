from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    user_first_name: str
    user_surname: str
    user_email: EmailStr
    user_cell: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    user_first_name: str | None = None
    user_surname: str | None = None
    user_email: EmailStr | None = None
    user_cell: str | None = None