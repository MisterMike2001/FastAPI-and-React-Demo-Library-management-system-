from app.models.genres_model import Genre


class GenreRepo:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_genres(self):
        return self.db_session.query(Genre).all()

    def get_genre_by_id(self, genre_id: int):
        return self.db_session.query(Genre).filter(Genre.genre_id == genre_id).first()

    def create_genre(self, item: Genre):
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def update_genre(self, genre_id: int, changes: Genre):
        item = self.get_genre_by_id(genre_id)
        if item is None:
            return None

        if changes.genre_name is not None:
            item.genre_name = changes.genre_name

        if changes.genre_descr is not None:
            item.genre_descr = changes.genre_descr

        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def delete_genre(self, genre_id: int):
        item = self.get_genre_by_id(genre_id)
        if item is None:
            return None
        self.db_session.delete(item)
        self.db_session.commit()
        return item
