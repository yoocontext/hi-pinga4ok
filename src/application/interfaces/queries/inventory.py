from typing import Protocol
from uuid import UUID

from application.entities.inventory_item import InventoryItem


class IInventoryQueries(Protocol):
    async def items(
        self,
        *,
        owner_id: UUID,
    ) -> list[InventoryItem]:
        """Return the owner's items, newest first."""
        ...
