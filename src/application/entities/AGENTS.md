# Entities guide

An entity is a plain dataclass with an `id` that guards its own invariants.
It is persisted through `dm`.

- Not a passive data holder: every rule about its state lives in the entity,
  not in use cases.
- Not a DDD model: no domain layer, aggregate roots, value objects, domain
  events, or factories.

## Shape

```python
@dataclass(frozen=True, kw_only=True)
class Order:
    id: UUID

    lines: tuple[OrderLine, ...]

    status: OrderStatus
    paid_at: datetime | None = None

    def mark_paid(self, *, at: datetime) -> Self:
        if self.status is not OrderStatus.PENDING:
            raise OrderNotPendingError(order_id=self.id)

        return replace(self, status=OrderStatus.PAID, paid_at=at)
```

- Group fields by meaning, separated by a blank line.
- Use `tuple` for collections; `frozen` does not protect list contents.
- Check state invariants in `__post_init__`.
- Change state only through entity methods that return a new instance via
  `replace`. Do not call `replace` on an entity outside its own methods.
- Pass time as an `at` argument.
- Generate new ids with `uuid.uuid7()`.

## File structure

One file per entity, grouped by domain: `entities/orders/order.py`.
Entities that exist only inside another entity live in its file.
Declare entity errors next to the entity.
