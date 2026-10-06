# Tests guide

## Structure

```text
tests/{test_type}/...
tests/fakes/...
tests/ioc/
  container.py
  providers/
```

- `{test_type}` — `unit`, `integration`, `e2e`.
- `tests/fakes/` mirrors `src/application/interfaces/`.
- `tests/ioc/container.py` builds the IoC container with fakes instead of
  real implementations.

## Test types

- `unit` — tests one function / class in isolation.
- `integration` — tests several parts together.
- `e2e` — tests a full scenario through an external entry point.

## What to test and how

| Component | Test type | How |
|---|---|---|
| entity | unit | directly, no fakes |
| service, use case | unit | fakes for dm, queries, and other interfaces |
| dm, queries | integration | against real Postgres (`just pg`) |
| handler | e2e | through the transport client |

## Fakes, not mocks

- Replace dependencies with fakes: in-memory implementations of application
  interfaces.
- Do not use `Mock` or `MagicMock` for application interfaces.
- Assert on returned values and resulting state, not on which methods were
  called.

## Grouping

Group files by meaning or entity.

Bad:

```text
test_create_duplicate_user.py
test_update_user.py
```

Good:

```text
user/test_create_duplicate.py
user/test_update.py
```
