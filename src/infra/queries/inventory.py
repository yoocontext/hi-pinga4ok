from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.entities.inventory_item import InventoryItem
from infra.dm.mappers.inventory_item import (
    inventory_item_from_orm,
    inventory_item_loading,
)
from infra.orm.inventory import InventoryItemOrm


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyInventoryQueries:
    session: AsyncSession

    async def items(
        self,
        *,
        owner_id: UUID,
    ) -> list[InventoryItem]:
        stmt = (
            select(InventoryItemOrm)
            .where(InventoryItemOrm.owner_id == owner_id)
            .options(inventory_item_loading())
            .order_by(InventoryItemOrm.obtained_at.desc())
        )

        orms = await self.session.scalars(stmt)

        return [inventory_item_from_orm(orm=orm) for orm in orms]
