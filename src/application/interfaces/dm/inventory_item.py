from typing import Protocol
from uuid import UUID

from application.entities.inventory_item import InventoryItem


class IInventoryItemDm(Protocol):
    async def get_for_update(
        self,
        *,
        id: UUID,
    ) -> InventoryItem | None: ...

    def add(
        self,
        *,
        entity: InventoryItem,
    ) -> None: ...

    async def save(
        self,
        *,
        entity: InventoryItem,
    ) -> None: ...
