"""Verify the current query-parameter routes without touching PostgreSQL."""
import unittest
from datetime import date
from importlib import import_module

from fastapi import HTTPException
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.main import app
from app.models.base_model import Base


class CurrentRouteTests(unittest.TestCase):
    def test_crud_and_missing_records(self):
        engine = create_engine('sqlite://')

        @event.listens_for(engine, 'connect')
        def enable_foreign_keys(connection, _):
            connection.execute('PRAGMA foreign_keys=ON')

        Base.metadata.create_all(engine)
        self.addCleanup(engine.dispose)
        db = Session(engine)
        self.addCleanup(db.close)
        cases = [
            ('authors', 'author', 'authors', 'author_id', dict(first_name='Jane', surname='Doe'), dict(surname='Smith')),
            ('genre', 'genre', 'genres', 'genre_id', dict(genre_name='Fiction', genre_descr='Stories'), dict(genre_descr='Updated')),
            ('inventory_status', 'inventory_status', 'inventory_status', 'inventory_status_id', dict(inventory_status_name='Available', inventory_status_descr='Ready'), dict(inventory_status_descr='Updated')),
            ('book', 'book', 'books', 'book_id', dict(book_name='Example', book_descr='Description', book_author_id=1, book_genre_id=1), dict(book_name='Updated')),
            ('customer', 'customer', 'customers', 'customer_id', dict(customer_first_name='Sam', customer_surname='Reader', customer_email='sam@example.com'), dict(customer_cell='123')),
            ('book_inventory', 'book_inventory', 'book_inventory', 'inventory_id', dict(book_id=1, inventory_status_id=1), dict(inventory_status_id=1)),
            ('book_loans', 'book_loan', 'book_loans', 'loan_id', dict(customer_id=1, inventory_id=1, date_loaned=date(2026, 1, 1), date_due=date(2026, 1, 15)), dict(date_returned=date(2026, 1, 10))),
        ]
        paths = app.openapi()['paths']
        for module, singular, plural, pk, values, changes in cases:
            with self.subTest(resource=plural):
                routes = import_module(f'app.routes.{module}_route')
                self.assertIn(f'/{plural}/create/', paths)
                item = getattr(routes, f'create_{singular}')(**values, db=db)
                self.assertEqual(getattr(item, pk), 1)
                self.assertEqual(len(getattr(routes, f'get_{plural}')(db=db)), 1)
                update = getattr(routes, f'update_{singular}')
                getattr(routes, f'get_{singular}_by_id')(**{pk: 1}, db=db)
                update(**{pk: 1}, **changes, db=db)
                db.expire_all()
                for field, value in changes.items():
                    column = 'author_surname' if field == 'surname' else field
                    self.assertEqual(getattr(item, column), value)
                for function in (getattr(routes, f'get_{singular}_by_id'), update, getattr(routes, f'delete_{singular}')):
                    with self.assertRaises(HTTPException) as error:
                        function(**{pk: 999}, db=db)
                    self.assertEqual(error.exception.status_code, 404)
        # Delete dependants first, with real foreign-key enforcement enabled.
        for module, singular, plural, pk, _, _ in reversed(cases):
            routes = import_module(f'app.routes.{module}_route')
            getattr(routes, f'delete_{singular}')(**{pk: 1}, db=db)
            with self.assertRaises(HTTPException) as error:
                getattr(routes, f'get_{plural}')(db=db)
            self.assertEqual(error.exception.status_code, 404)


if __name__ == '__main__':
    unittest.main()
