# PostgreSQL ORM

These instructions apply to SQLAlchemy ORM models under
`src/infra/orm/**`.

## Declaration Order

- Inside each ORM class, keep declarations grouped in this order:
  primary key columns, blank line, `relationship(...)` attributes, blank line,
  `ForeignKey(...)` columns, blank line, regular table columns.

## File Structure

- Do not collect unrelated ORM models in one large file.
- Split ORM models by domain, for example `orders`, `billing`, `catalog`.
- Keep models that change together in the same file.
- Link models across files through typed forward references instead of
  merging domains into one file.

## Relationship Rules

- Keep SQLAlchemy relationships explicit with `back_populates` on both sides.
- Use database-level `ForeignKey(..., ondelete="CASCADE")` only when domain
  rules require deleting dependent records with their parent. `CASCADE` is
  not the default for every foreign key.
- Add ORM `cascade` only on owner-side collection relationships, for example
  `OrderOrm.lines`.
- Use `passive_deletes=True` with DB cascades so SQLAlchemy does not need to
  load child collections just to delete a parent.
- dm and queries filter by FK columns directly instead of loading
  relationships. ORM models and their relationships never leave infra.
