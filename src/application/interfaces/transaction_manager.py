from collections.abc import (
    Iterable,
    Sequence,
)
from typing import Protocol


class ITransactionManager(Protocol):
    def add(
        self,
        *,
        instance: object,
    ) -> None: ...

    def add_all(
        self,
        *,
        instances: Iterable[object],
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def flush(
        self,
        *,
        objects: Sequence[object] | None = None,
    ) -> None: ...

    async def refresh(
        self,
        *,
        instance: object,
        attribute_names: Iterable[str] | None = None,
    ) -> None: ...
