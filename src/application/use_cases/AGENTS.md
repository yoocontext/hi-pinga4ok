# Use Cases guide

A use case runs one scenario end to end and owns its transaction. See
"Where logic goes" in `application/AGENTS.md`.

## Shape

- One file holds the command `XCm`, the result `XRs`, and the use case `XUc`.
- Declare `Cm` and `Rs` with `@dataclass(frozen=True, kw_only=True)`.
- Inherit `BaseUseCase[XCm, XRs]` from `use_cases/base.py`. Use `None` as the
  result type when nothing is returned.
- Declare the use case as a `@dataclass` and inject dependencies as protected
  fields: `_order_dm: IOrderDm`.
- Commit once, at the end of the scenario.

## Time

- Only use cases read the current time, through `IClock`. Pass it down as
  `at`.
- Put `at` in `Cm` only when the caller defines the moment, for example a job
  that processes a given date.

## Mapping

- Build `Rs` in the use case when it only passes fields.
- Move mapping with nested results, collections, or computed values into a
  mapper that mirrors the use case path:

  ```text
  use_cases/payments/invoice/create.py
  → use_cases/mappers/payments/invoice/create.py
  ```

## File structure

One file → one use case. Group by feature; create entity subdirectories only
when an entity has several use cases.

```text
use_cases/payments/create_invoice.py
use_cases/payments/invoice/create.py
use_cases/payments/invoice/delete.py
```

Queries follow this grouping, see `infra/queries/AGENTS.md`.
