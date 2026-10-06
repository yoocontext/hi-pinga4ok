# IoC guide

## Structure

```text
src/bootstrap/ioc/
  container.py          create_container() lists every provider
  providers/{layer}/... mirrors src/ by layer
```

A provider file groups wiring for one kind of component or one feature:

```text
src/infra/dm/...                → providers/infra/dm.py
src/infra/queries/...           → providers/infra/queries.py
src/application/use_cases/...   → providers/application/use_cases.py
```

Split a provider file by feature when it grows:
`providers/infra/dm/orders.py`.

## Providers

```python
class DmProvider(Provider):
    order_dm = provide(
        AlchemyOrderDm,
        provides=IOrderDm,
        scope=Scope.REQUEST,
    )


class UseCasesProvider(Provider):
    pay_order = provide(PayOrderUc, scope=Scope.REQUEST)
```

- Provide the interface, not the implementation: `provides=IOrderDm`.
- Use `Scope.APP` for settings, engine, session factory, clients, and clock.
- Use `Scope.REQUEST` for the session and everything that depends on it:
  transaction manager, dm, queries, services, use cases.
- A provider that opens a resource yields it and closes it after `yield`.
- Add every new provider to `create_container()`.
- Do not add constructor arguments to providers for tests; tests replace
  providers in `tests/ioc/`.

Handlers receive use cases through `FromDishka[PayOrderUc]` with `@inject`.
