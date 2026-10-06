# Delivery layer guide

## Structure

```text
src/delivery/api/v{version}/{transport}/
```

Examples:

```text
api/v1/http/
api/v1/grpc/
api/v1/events/
```

- `handlers.py` → few endpoints.
- `handlers/` → multiple entities or workflows.
- `schemas/{endpoint}.py`
- `mappers/{endpoint}.py`

Use matching names for endpoint, schema, and mapper files.

## Handlers

A handler only calls a use case:

```text
request schema → mapper → Cm → use case → Rs → mapper → response schema
```

- No business logic. Do not call dm, queries, or services; reads go through
  use cases too.
- Do not catch application errors in handlers.

## Errors

Each transport maps errors in one file, for example `api/v1/http/errors.py`:

- application errors → status by category, body
  `{"error": {"code", "message", "details"}}`;
- request validation errors → 422 in the same shape;
- anything else → 500 without details.

Handlers are registered once in `bootstrap/app.py`. Do not add per-error
handlers; a new error only needs the right category.
