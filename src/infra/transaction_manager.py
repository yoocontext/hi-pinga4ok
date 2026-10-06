from collections.abc import (
    Iterable,
    Sequence,
)
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyTransactionManager:
    session: AsyncSession

    def add(
        self,
        *,
        instance: object,
    ) -> None:
        self.session.add(instance)

    def add_all(
        self,
        *,
        instances: Iterable[object],
    ) -> None:
        self.session.add_all(instances)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(
        self,
        *,
        objects: Sequence[object] | None = None,
    ) -> None:
        await self.session.flush(objects)

    async def refresh(
        self,
        *,
        instance: object,
        attribute_names: Iterable[str] | None = None,
    ) -> None:
        await self.session.refresh(instance, attribute_names)
