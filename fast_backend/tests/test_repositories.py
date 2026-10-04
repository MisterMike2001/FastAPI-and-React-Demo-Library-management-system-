"""Exercise repository behavior using SQLite with foreign keys enabled."""

import unittest
from datetime import date

from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import repositories as repos, schemas
from app.models.base_model import Base


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")

        @event.listens_for(self.engine, "connect")
        def enable_foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine, autoflush=False)
        self.addCleanup(self.engine.dispose)
        self.addCleanup(self.db.close)
        self.cases = [
            ("Author", dict(author_first_name="Ursula", author_surname="Le Guin")),
            ("Genre", dict(genre_name="Fantasy", genre_descr="Fantasy books")),
            ("InventoryStatus", dict(inventory_status_name="Available", inventory_status_descr="Ready to borrow")),
            ("Book", dict(book_name="Earthsea", book_descr="A novel", book_isbn="9780000000001", book_genre_id=1, book_author_id=1)),
            ("Customer", dict(customer_first_name="Jane", customer_surname="Doe", customer_email="jane@example.com", customer_cell="123")),
            ("BookInventory", dict(book_id=1, inventory_status_id=1)),
            ("BookLoan", dict(customer_id=1, inventory_id=1, date_loaned=date(2026, 9, 20), date_due=date(2026, 10, 4))),
            ("User", dict(username="librarian", user_first_name="Alex", user_surname="Doe", user_email="alex@example.com", password="secret")),
        ]
        for name, values in self.cases:
            repository = getattr(repos, f"{name}Repository")(self.db)
            options = {"password_hash": "hashed-password"} if name == "User" else {}
            repository.create(getattr(schemas, f"{name}Create")(**values), **options)
        self.db.commit()

    def test_crud_for_every_resource(self):
        for name, values in self.cases:
            with self.subTest(resource=name):
                repository = getattr(repos, f"{name}Repository")(self.db)
                values = values.copy()
                for field in ("genre_name", "inventory_status_name", "book_isbn", "customer_email", "username", "user_email"):
                    if field in values:
                        values[field] = "other-" + values[field]
                options = {"password_hash": "another-hash"} if name == "User" else {}
                record = repository.create(getattr(schemas, f"{name}Create")(**values), **options)
                pk = next(iter(repository.model.__table__.primary_key.columns)).name
                record_id = getattr(record, pk)
                self.assertEqual(record_id, 2)
                self.assertIs(repository.get_by_id(record_id), record)
                self.assertEqual(repository.get_all(offset=1, limit=1), [record])
                field = next(key for key in values if key != "password")
                value = values[field]
                replacement = "Updated" if isinstance(value, str) else value
                patch = getattr(schemas, f"{name}Update")(**{field: replacement})
                self.assertIs(repository.update(record_id, patch), record)
                self.db.expire_all()
                self.assertEqual(getattr(record, field), replacement)
                self.assertTrue(repository.delete(record_id))
                self.assertIsNone(repository.get_by_id(record_id))
                self.assertFalse(repository.delete(record_id))
                self.assertIsNone(repository.update(999, patch))
                self.assertIsNone(repository.get_by_id(999))

    def test_partial_update_preserves_omitted_fields_and_clears_nulls(self):
        repository = repos.CustomerRepository(self.db)
        customer = repository.update(1, schemas.CustomerUpdate(customer_cell=None))
        self.db.expire_all()
        self.assertIsNone(customer.customer_cell)
        self.assertEqual(customer.customer_first_name, "Jane")
        self.assertEqual(customer.customer_email, "jane@example.com")

    def test_mutations_can_be_rolled_back(self):
        repository = repos.AuthorRepository(self.db)
        author = repository.create(schemas.AuthorCreate(author_first_name="New", author_surname="Author"))
        record_id = author.author_id
        self.db.rollback()
        self.assertIsNone(repository.get_by_id(record_id))
        repository.update(1, schemas.AuthorUpdate(author_surname="Changed"))
        self.db.rollback()
        self.assertEqual(repository.get_by_id(1).author_surname, "Le Guin")
        user_repository = repos.UserRepository(self.db)
        user_repository.delete(1)
        self.db.rollback()
        self.assertIsNotNone(user_repository.get_by_id(1))

    def test_unique_and_foreign_key_failures_are_propagated(self):
        with self.assertRaises(IntegrityError):
            repos.GenreRepository(self.db).create(schemas.GenreCreate(genre_name="Fantasy", genre_descr="Duplicate"))
        self.db.rollback()
        with self.assertRaises(IntegrityError):
            repos.BookInventoryRepository(self.db).create(schemas.BookInventoryCreate(book_id=999, inventory_status_id=1))
        self.db.rollback()
        # A referenced parent cannot silently delete its dependent rows.
        with self.assertRaises(IntegrityError):
            repos.AuthorRepository(self.db).delete(1)
        self.db.rollback()
        self.assertIsNotNone(repos.BookRepository(self.db).get_by_id(1))

    def test_resource_lookups(self):
        self.assertEqual(len(repos.AuthorRepository(self.db).get_by_name("Ursula", "Le Guin")), 1)
        self.assertEqual(repos.AuthorRepository(self.db).get_by_name("Missing", "Author"), [])
        self.assertIsNotNone(repos.GenreRepository(self.db).get_by_name("Fantasy"))
        self.assertIsNotNone(repos.InventoryStatusRepository(self.db).get_by_name("Available"))
        books = repos.BookRepository(self.db)
        self.assertIsNotNone(books.get_by_isbn("9780000000001"))
        self.assertIsNone(books.get_by_isbn("missing"))
        self.assertEqual(len(books.get_by_author(1)), 1)
        self.assertEqual(books.get_by_genre(999), [])
        self.assertIsNotNone(repos.CustomerRepository(self.db).get_by_email("jane@example.com"))
        inventory = repos.BookInventoryRepository(self.db)
        self.assertEqual(len(inventory.get_by_book(1)), 1)
        self.assertEqual(len(inventory.get_by_status(1)), 1)
        loans = repos.BookLoanRepository(self.db)
        self.assertEqual(len(loans.get_by_customer(1)), 1)
        self.assertEqual(len(loans.get_by_inventory(1)), 1)
        self.assertEqual(len(loans.get_active()), 1)
        loans.update(1, schemas.BookLoanUpdate(date_returned=date(2026, 9, 21)))
        self.assertEqual(loans.get_active(), [])
        users = repos.UserRepository(self.db)
        self.assertIsNotNone(users.get_by_username("librarian"))
        self.assertIsNotNone(users.get_by_email("alex@example.com"))

    def test_user_password_requires_service_hash(self):
        repository = repos.UserRepository(self.db)
        with self.assertRaises(ValueError):
            repository.update(1, schemas.UserUpdate(password="new-secret"))
        user = repository.update(1, schemas.UserUpdate(password="new-secret"), password_hash="new-hash")
        self.assertEqual(user.password_hash, "new-hash")
        self.assertFalse(hasattr(user, "password"))
        repository.update(1, schemas.UserUpdate(user_surname="Changed"))
        self.assertEqual(user.password_hash, "new-hash")
        with self.assertRaises(ValueError):
            repository.update(1, schemas.UserUpdate(), password_hash="")

    def test_pagination_validation(self):
        repository = repos.BookRepository(self.db)
        for options in ({"offset": -1}, {"limit": 0}):
            with self.assertRaises(ValueError):
                repository.get_all(**options)
            with self.assertRaises(ValueError):
                repository.get_by_author(1, **options)


if __name__ == "__main__":
    unittest.main()
