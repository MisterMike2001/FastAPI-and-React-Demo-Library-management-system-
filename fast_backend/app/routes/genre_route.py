from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.models.genres_model import Genre
from app.repositories.genre_repo import GenreRepo

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/")
def get_genres(db: Session = Depends(get_db)):
    repo = GenreRepo(db)
    items = repo.get_all_genres()
    if not items:
        raise HTTPException(status_code=404, detail="No genres found")
    return items


@router.get("/{genre_id}")
def get_genre_by_id(genre_id: int, db: Session = Depends(get_db)):
    repo = GenreRepo(db)
    item = repo.get_genre_by_id(genre_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return item


@router.put("/update/{genre_id}")
def update_genre(
    genre_id: int,
    genre_name: str | None = None,
    genre_descr: str | None = None,
    db: Session = Depends(get_db),
):
    repo = GenreRepo(db)
    changes = Genre(
        genre_name=genre_name,
        genre_descr=genre_descr,
    )
    item = repo.update_genre(genre_id, changes)
    if item is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return item


@router.post("/create/", status_code=201)
def create_genre(
    genre_name: str,
    genre_descr: str,
    db: Session = Depends(get_db),
):
    repo = GenreRepo(db)
    item = Genre(
        genre_name=genre_name,
        genre_descr=genre_descr,
    )
    return repo.create_genre(item)


@router.delete("/delete/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    repo = GenreRepo(db)
    item = repo.delete_genre(genre_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return {"message": "Genre deleted"}
