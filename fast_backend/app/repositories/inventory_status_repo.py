from app.models.inventory_status_model import InventoryStatus


class InventoryStatusRepo:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_inventory_status(self):
        return self.db_session.query(InventoryStatus).all()

    def get_inventory_status_by_id(self, inventory_status_id: int):
        return self.db_session.query(InventoryStatus).filter(InventoryStatus.inventory_status_id == inventory_status_id).first()

    def create_inventory_status(self, item: InventoryStatus):
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def update_inventory_status(self, inventory_status_id: int, changes: InventoryStatus):
        item = self.get_inventory_status_by_id(inventory_status_id)
        if item is None:
            return None

        if changes.inventory_status_name is not None:
            item.inventory_status_name = changes.inventory_status_name

        if changes.inventory_status_descr is not None:
            item.inventory_status_descr = changes.inventory_status_descr

        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def delete_inventory_status(self, inventory_status_id: int):
        item = self.get_inventory_status_by_id(inventory_status_id)
        if item is None:
            return None
        self.db_session.delete(item)
        self.db_session.commit()
        return item
