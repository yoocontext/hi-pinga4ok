# Project architecture

- bootstrap — application assembly and dependency wiring.
- delivery — transport layer: controllers, schemas, validation, auth.
- application — business use cases and orchestration.
- infra — external integrations and implementations.

## Layer dependencies

- bootstrap — knows all layers.
- delivery — may know only application.
- application — knows only its own contracts and pure application code.
- infra — knows application contracts and implements external integrations.

### Import rule

- Import only layers listed above.

## Transaction boundaries

- Services, dm, and queries share the caller's database session. A
  `commit()` or `rollback()` inside them affects the caller's entire
  transaction and may break the atomicity of the scenario.
- Choose transaction boundaries with the calling scenario in mind. When a
  component needs an independent commit or rollback, use a separate session
  and make that transaction ownership explicit in its contract.

## src/bootstrap

- Assembly layer, entrypoint.
- Register all new dependencies in `bootstrap/ioc/`.
- Do not instantiate dependencies outside IoC.

## File and folder granularity

### File structure

Prefer small files.

Organize code by feature or domain, then by entity.

```text
payments/tax.py
payments/user/tax.py
```

Refactor freely as the domain evolves:

```text
users.py
→ users/tax.py
→ payments/users/tax.py
```

Do not preserve file structure for backward compatibility. Prefer correct
ownership and cohesion.

## Code rules

Do not create `helpers` or `utils` packages.

Avoid nested classes and nested functions.

Do not introduce constants for configuration values.
Add them to `src/bootstrap/settings.py`: a `pydantic` model per area nested in
the root `Settings` and read from `.dev.env` as `{AREA}__{FIELD}`.

## Readability

Public methods read as a scenario: a short sequence of named steps. Move
mechanics into private methods, functions, or other components.

```python
async def renew(
    self,
    *,
    subscription: Subscription,
    at: datetime,
) -> Payment:
    payment = self._create_payment(
        subscription=subscription,
        at=at,
    )

    # provider rejects repeated charges without the same key
    key = self._idempotency_key(payment=payment)

    await self._provider.charge(
        payment=payment,
        key=key,
    )

    return payment
```

- Keep one level of abstraction per method: do not mix scenario steps with
  low-level details.
- Name methods by what they do in the domain: `charge_renewal`, not
  `process` or `handle_data`.
- A private method is either a named scenario step or hides a non-trivial
  mechanism. Do not add one-line wrappers that only rename a call.
- Do not write defensive code for states that types or invariants already
  exclude.

## Formatting

`ruff format` joins a bracketed construct into one line when it fits, unless
the last element has a trailing comma. Code stays vertical on purpose: write
the trailing comma and the formatter keeps the layout.

### One element per line

Put each element on its own line, indented once, and end with a trailing
comma in:

- `from x import (...)` with two or more names;
- signatures with any parameter besides `self` or `cls`;
- calls with two or more keyword arguments;
- class definitions with two or more bases;
- dict literals with two or more keys;
- method chains with two or more calls: wrap them in parentheses, one call
  per line, each line starting with `.`.

Keep a construct on one line when it has a single element:
`from x import Y`, `def total(self) -> int:`, `Text(content=content)`.

### Keyword-only parameters

- Put `*` right after `self` or `cls`, or first in a plain function, so
  callers must pass arguments by name.
- Pass arguments by name when calling project code. In third-party calls the
  main positional argument may stay positional: `select(TextOrm)`,
  `session.add(instance)`.
- Skip `*` only in dunder methods and where a framework passes arguments
  positionally.

### Blank lines

Blank lines split code into steps. Put exactly one blank line:

- before `return`, `raise` and `yield`, unless it is the only statement in
  its block;
- before and after a statement that spans several lines;
- before and after `if`, `for`, `while`, `with`, `try` and `match` blocks;
- between a `try` body and each `except`, `else` and `finally`;
- between steps of a scenario.

Lines that form one step stay together. Never put a blank line right after a
line ending with `:`, right inside brackets, or twice in a row inside a
function or class.

```python
from sqlalchemy import (
    Select,
    select,
)


@dataclass(kw_only=True)
class TextQueries(
    BaseQueries,
    ITextQueries,
):
    session: AsyncSession

    async def last(
        self,
        *,
        count: int,
    ) -> list[Text]:
        stmt = (
            select(TextOrm)
            .order_by(TextOrm.created_at.desc())
            .limit(count)
        )

        rows = await self.session.scalars(stmt)

        if not rows:
            raise TextNotFoundError()

        return [self._to_entity(row=row) for row in rows]
```

## Docstrings and comments

- Add a docstring to a class, method, or function only when it makes the
  component easier to understand: what it does and why, in a few lines.
  Skip it when the name already says that.
- Comment only what the code cannot say: why a step exists, workarounds,
  hardcoded values, and special cases. Keep comments short and lowercase,
  with a blank line before each.

## Git rules

- Base branch: `dev`. Branch from `dev` and open pull requests into `dev`.
- `main` receives releases only.
- Branch names: `feat/{short-name}` for features, `fix/{short-name}` for fixes.
  Use kebab-case for `{short-name}`.
