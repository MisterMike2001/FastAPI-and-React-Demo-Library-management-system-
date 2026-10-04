from app.models.book_loans_model import BookLoan


class BookLoanRepo:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_book_loans(self):
        return self.db_session.query(BookLoan).all()

    def get_book_loan_by_id(self, loan_id: int):
        return self.db_session.query(BookLoan).filter(BookLoan.loan_id == loan_id).first()

    def create_book_loan(self, item: BookLoan):
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def update_book_loan(self, loan_id: int, changes: BookLoan):
        item = self.get_book_loan_by_id(loan_id)
        if item is None:
            return None

        if changes.customer_id is not None:
            item.customer_id = changes.customer_id

        if changes.inventory_id is not None:
            item.inventory_id = changes.inventory_id

        if changes.date_loaned is not None:
            item.date_loaned = changes.date_loaned

        if changes.date_due is not None:
            item.date_due = changes.date_due

        if changes.date_returned is not None:
            item.date_returned = changes.date_returned

        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def delete_book_loan(self, loan_id: int):
        item = self.get_book_loan_by_id(loan_id)
        if item is None:
            return None
        self.db_session.delete(item)
        self.db_session.commit()
        return item
