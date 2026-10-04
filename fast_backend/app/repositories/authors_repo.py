

from app.models.authors_model import Author


class AuthorsRepo:
    def __init__(self, db):
        self.db = db

    def get_authors(self):
        return self.db.query(Author).all()
    
    def get_author_by_id(self, author_id):
        return self.db.query(Author).filter(Author.author_id == author_id).first()

    def update_author(self, author_id, first_name=None, surname=None):
        author = self.get_author_by_id(author_id)
        if author:
            if first_name is not None:
                author.author_first_name = first_name
            if surname is not None:
                author.author_surname = surname
            self.db.commit()
            self.db.refresh(author)
            return author
        return None
    
    def create_author(self, first_name, surname):
        author = Author(author_first_name=first_name, author_surname=surname)
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def delete_author(self, author_id: int):
        item = self.get_author_by_id(author_id)
        if item is None:
            return None
        self.db.delete(item)
        self.db.commit()
        return item
