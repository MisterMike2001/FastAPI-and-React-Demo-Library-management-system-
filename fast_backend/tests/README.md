# API schemas

Each resource has `Create`, `Update`, and `Read` schemas, exported from
`app.schemas`. Field names and string length limits match the database models.
Read schemas accept ORM instances with `Schema.model_validate(instance)` and
contain foreign key IDs rather than nested relationships.

```python
from app.schemas import AuthorCreate, AuthorRead, AuthorUpdate

payload = AuthorCreate(author_first_name="Ursula", author_surname="Le Guin")
values = payload.model_dump()

patch = AuthorUpdate(author_surname="Le Guin")
changes = patch.model_dump(exclude_unset=True)
```

Always use `exclude_unset=True` when applying updates. Omitted fields are left
unchanged. Explicit `None` clears nullable columns (ISBN, cell numbers, or return
date); it is rejected for required database columns. Unknown request fields,
including generated primary keys, are rejected.

User create/update schemas accept `password` as `SecretStr`. The service must
extract it with `get_secret_value()`, hash it, and store the resulting
`password_hash`. Do not pass a user payload directly to the ORM constructor.
`UserRead` exposes neither the password nor its hash.

Email fields currently enforce the database's length limit, not email syntax.
Uniqueness, foreign key existence, and loan date rules belong in the database
and service layer; these schemas do not query the database.

Run the schema checks from `fast_backend`:

```sh
.venv/bin/python -m unittest discover -s tests -v
```
