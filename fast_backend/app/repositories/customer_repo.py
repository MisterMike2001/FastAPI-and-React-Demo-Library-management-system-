from app.models.customers_model import Customer


class CustomerRepo:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_customers(self):
        return self.db_session.query(Customer).all()

    def get_customer_by_id(self, customer_id: int):
        return self.db_session.query(Customer).filter(Customer.customer_id == customer_id).first()

    def create_customer(self, item: Customer):
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def update_customer(self, customer_id: int, changes: Customer):
        item = self.get_customer_by_id(customer_id)
        if item is None:
            return None

        if changes.customer_first_name is not None:
            item.customer_first_name = changes.customer_first_name

        if changes.customer_surname is not None:
            item.customer_surname = changes.customer_surname

        if changes.customer_email is not None:
            item.customer_email = changes.customer_email

        if changes.customer_cell is not None:
            item.customer_cell = changes.customer_cell

        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def delete_customer(self, customer_id: int):
        item = self.get_customer_by_id(customer_id)
        if item is None:
            return None
        self.db_session.delete(item)
        self.db_session.commit()
        return item
