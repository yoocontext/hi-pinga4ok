from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.entities.inventory_item import InventoryItem
from infra.dm.mappers.inventory_item import (
    inventory_item_from_orm,
    inventory_item_loading,
    inventory_item_to_orm,
)
from infra.orm.inventory import InventoryItemOrm


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyInventoryItemDm:
    session: AsyncSession

    async def get_for_update(
        self,
        *,
        id: UUID,
    ) -> InventoryItem | None:
        stmt = (
            select(InventoryItemOrm)
            .where(InventoryItemOrm.id == id)
            .options(inventory_item_loading())
            # lock only the inventory row; the joined catalog item is shared
            # by every copy and must stay free for other players
            .with_for_update(of=InventoryItemOrm)
            .execution_options(populate_existing=True)
        )

        orm = await self.session.scalar(stmt)

        return None if orm is None else inventory_item_from_orm(orm=orm)

    def add(
        self,
        *,
        entity: InventoryItem,
    ) -> None:
        self.session.add(inventory_item_to_orm(entity=entity))

    async def save(
        self,
        *,
        entity: InventoryItem,
    ) -> None:
        await self.session.merge(inventory_item_to_orm(entity=entity))
