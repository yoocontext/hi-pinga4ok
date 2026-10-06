# Data mappers (dm)

## Purpose

A `dm` loads and persists one entity or aggregate and maps it to and from ORM
models.

Feature-specific reads and multi-row writes do not belong here; put them in
`../queries/`.

## Methods

A dm may expose only these methods. Implement only the ones you need.

- `get(*, id)` — entity or `None`.
- `get_for_update(*, id)` — entity or `None`; the row stays locked until the
  transaction ends.
- `add(*, entity)` — stage a new entity.
- `save(*, entity)` — persist changes to an existing entity.
- `delete(*, entity)` — stage deletion.

Any other method is a query. Add it to `../queries/` instead.

## Restrictions

- Accept and return application entities, never ORM models.
- Do not call `commit()` or `rollback()`. See "Transaction boundaries" in the
  root `AGENTS.md`.
- Do not make business decisions: no policies, clocks, or settings.

## Mapping

- Keep ORM ↔ entity mapping in `mappers/`, not in dm classes.
- `../queries/` reuses these mappers when returning entities.

## File structure

One entity → one interface, one dm, one mapper.

```text
application/interfaces/dm/payment.py   IPaymentDm
infra/dm/payment.py                    AlchemyPaymentDm
infra/dm/mappers/payment.py
```
