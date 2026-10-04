from fastapi import FastAPI

from app.models.authors_model import Author
from app.models.books_model import Book
from app.models.genres_model import Genre
from app.models.book_inventory_model import BookInventory
from app.models.inventory_status_model import InventoryStatus
from app.models.book_loans_model import BookLoan
from app.models.customers_model import Customer
from app.models.users_model import User

from app.routes.authors_route import router as authors_router
from app.routes.book_route import router as book_router

from app.routes.genre_route import router as genre_router
from app.routes.customer_route import router as customer_router
from app.routes.inventory_status_route import router as inventory_status_router
from app.routes.book_inventory_route import router as book_inventory_router
from app.routes.book_loans_route import router as book_loans_router

app = FastAPI(
    title="Library Management API",
    description="Backend API for the Library Management System",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Library Management API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(authors_router)
app.include_router(book_router)
app.include_router(genre_router)
app.include_router(customer_router)
app.include_router(inventory_status_router)
app.include_router(book_inventory_router)
app.include_router(book_loans_router)
