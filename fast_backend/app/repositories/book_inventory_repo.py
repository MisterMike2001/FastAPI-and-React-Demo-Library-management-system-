from app.models.book_inventory_model import BookInventory


class BookInventoryRepo:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_book_inventory(self):
        return self.db_session.query(BookInventory).all()

    def get_book_inventory_by_id(self, inventory_id: int):
        return self.db_session.query(BookInventory).filter(BookInventory.inventory_id == inventory_id).first()

    def create_book_inventory(self, item: BookInventory):
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def update_book_inventory(self, inventory_id: int, changes: BookInventory):
        item = self.get_book_inventory_by_id(inventory_id)
        if item is None:
            return None

        if changes.book_id is not None:
            item.book_id = changes.book_id

        if changes.inventory_status_id is not None:
            item.inventory_status_id = changes.inventory_status_id

        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def delete_book_inventory(self, inventory_id: int):
        item = self.get_book_inventory_by_id(inventory_id)
        if item is None:
            return None
        self.db_session.delete(item)
        self.db_session.commit()
        return item
