# Queries

## Purpose

Queries hold database access that a feature needs beyond loading or storing a
single entity: filtered lists, lookups by non-id fields, existence checks,
aggregates, joins, read models, and multi-row writes.

Loading or storing one entity belongs in `../dm/`.

## Grouping

One feature → one interface, one queries class.

Features follow the grouping of `application/use_cases/`:

```text
application/use_cases/billing/autopay/...
→ application/interfaces/queries/billing/autopay.py   IAutopayQueries
→ infra/queries/billing/autopay.py                     AlchemyAutopayQueries
```

- Add a method to the queries class of the feature that needs it.
- Do not use another feature's queries; give each feature its own method.
- When a queries class grows large, split the feature in `use_cases/` and
  split its queries the same way.

## Methods

- Name read methods by what they return: `due`, `history`, `sent_ids`,
  `has_unknown_send`.
- Name write methods with a verb: `stop_by_saga`, `prepare`.
- Pass every criterion as a parameter: time, limits, statuses. Do not read
  clocks or settings.
- Return entities, ids, primitives, or result dataclasses declared next to
  the interface. Never return ORM models or rows.

## Writes

Prefer loading an entity through dm, changing it, and calling `dm.save`.

Write in queries only when the change must be set-based: bulk updates,
upserts, or conditional updates that guard against races.

## Mapping

- Do not keep mapping details in queries classes.
- Entities: reuse `../dm/mappers/`. Do not create a second mapper for an
  entity.
- Result dataclasses: map them in `mappers/`, mirroring the queries
  structure:

  ```text
  infra/queries/billing/history.py
  infra/queries/mappers/billing/history.py
  ```

- Ids and primitives need no mapper.

## Sharing SQL

When two features need the same SQL, extract it into a module-level function
that takes `session`, and call it from both queries classes. Name the file
after the entity it queries.

```text
infra/queries/billing/payments.py   async def due_payment_ids(session, *, at, limit)
infra/queries/billing/autopay.py    AlchemyAutopayQueries.due → due_payment_ids(...)
```

## Restrictions

- Do not call `commit()` or `rollback()`.
- Do not make business decisions: the use case decides, queries fetch.
