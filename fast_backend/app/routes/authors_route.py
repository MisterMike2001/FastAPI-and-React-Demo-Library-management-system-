from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.repositories.authors_repo import AuthorsRepo


router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/")
def get_authors(db: Session = Depends(get_db)):
    auth_repo = AuthorsRepo(db)
    authors = auth_repo.get_authors()

    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")
    
    return authors


@router.get("/{author_id}")
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author_repo = AuthorsRepo(db)
    author = author_repo.get_author_by_id(author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@router.put("/update/{author_id}")
def update_author(author_id: int, first_name: str = None, surname: str = None, db: Session = Depends(get_db)):
    author_repo = AuthorsRepo(db)
    updated_author = author_repo.update_author(author_id, first_name, surname)

    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return updated_author

@router.post("/create/", status_code=201)
def create_author(first_name: str, surname: str, db: Session = Depends(get_db)):
    author_repo = AuthorsRepo(db)
    new_author = author_repo.create_author(first_name, surname)

    return new_author


@router.delete("/delete/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    repo = AuthorsRepo(db)
    item = repo.delete_author(author_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": "Author deleted"}
