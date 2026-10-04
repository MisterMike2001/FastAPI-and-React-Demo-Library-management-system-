"""Schema contracts checked against the actual SQLAlchemy models, without a DB."""

import unittest
from datetime import date
from importlib import import_module

from pydantic import ValidationError
from sqlalchemy import String

from app import schemas


RESOURCES = [
    ("authors", "Author"),
    ("genres", "Genre"),
    ("inventory_status", "InventoryStatus"),
    ("books", "Book"),
    ("customers", "Customer"),
    ("book_inventory", "BookInventory"),
    ("book_loans", "BookLoan"),
    ("users", "User"),
]
MODELS = {
    name: getattr(import_module(f"app.models.{module}_model"), name)
    for module, name in RESOURCES
}


def sample_values(model):
    values = {}
    for column in model.__table__.columns:
        if column.type.python_type is int:
            values[column.name] = 1
        elif column.type.python_type is date:
            values[column.name] = date(2026, 9, 20)
        else:
            values[column.name] = "sample"
    return values


class SchemaTests(unittest.TestCase):
    def test_create_and_read_match_database_fields(self):
        for name, model in MODELS.items():
            with self.subTest(resource=name):
                values = sample_values(model)
                read = getattr(schemas, f"{name}Read").model_validate(model(**values))
                expected = values.copy()
                expected.pop("password_hash", None)
                self.assertEqual(read.model_dump(), expected)

                for column in model.__table__.columns:
                    if column.primary_key:
                        expected.pop(column.name)
                if name == "User":
                    expected["password"] = "example-password"
                create = getattr(schemas, f"{name}Create")
                create.model_validate(expected)
                for column in model.__table__.columns:
                    if column.nullable or column.primary_key or column.name == "password_hash":
                        continue
                    incomplete = expected.copy()
                    incomplete.pop(column.name)
                    with self.assertRaises(ValidationError):
                        create.model_validate(incomplete)

    def test_partial_updates_and_nullability(self):
        for name, model in MODELS.items():
            update = getattr(schemas, f"{name}Update")
            self.assertEqual(update().model_dump(exclude_unset=True), {})
            for column in model.__table__.columns:
                if column.primary_key or column.name == "password_hash":
                    continue
                with self.subTest(resource=name, field=column.name):
                    payload = {column.name: None}
                    if column.nullable:
                        self.assertEqual(
                            update(**payload).model_dump(exclude_unset=True), payload
                        )
                    else:
                        with self.assertRaises(ValidationError):
                            update(**payload)

    def test_column_lengths_and_protected_fields(self):
        for name, model in MODELS.items():
            update = getattr(schemas, f"{name}Update")
            for column in model.__table__.columns:
                with self.subTest(resource=name, field=column.name):
                    if column.primary_key or column.name == "password_hash":
                        with self.assertRaises(ValidationError):
                            update(**{column.name: 1})
                    elif isinstance(column.type, String):
                        with self.assertRaises(ValidationError):
                            update(**{column.name: "x" * (column.type.length + 1)})

    def test_password_input_is_masked_and_not_in_responses(self):
        update = schemas.UserUpdate(password="example-password")
        self.assertEqual(update.password.get_secret_value(), "example-password")
        self.assertNotIn("example-password", update.model_dump_json())
        self.assertNotIn("password", schemas.UserRead.model_fields)
        self.assertNotIn("password_hash", schemas.UserRead.model_fields)
        for invalid in (None, ""):
            with self.assertRaises(ValidationError):
                schemas.UserUpdate(password=invalid)

    def test_dates_and_positive_foreign_keys(self):
        loan = schemas.BookLoanCreate(
            customer_id=1,
            inventory_id=2,
            date_loaned="2026-09-20",
            date_due="2026-10-04",
        )
        self.assertEqual(loan.date_loaned, date(2026, 9, 20))
        self.assertIsNone(loan.date_returned)
        with self.assertRaises(ValidationError):
            schemas.BookLoanUpdate(date_due="not-a-date")
        with self.assertRaises(ValidationError):
            schemas.BookInventoryCreate(book_id=0, inventory_status_id=1)

    def test_all_public_schemas_generate_json_schema(self):
        for name in schemas.__all__:
            with self.subTest(schema=name):
                self.assertEqual(getattr(schemas, name).model_json_schema()["type"], "object")


if __name__ == "__main__":
    unittest.main()
