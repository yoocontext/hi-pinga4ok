from dataclasses import (
    dataclass,
    replace,
)
from datetime import datetime
from typing import Self
from uuid import UUID

from application.entities.item import Item
from application.exceptions import (
    AccessDeniedError,
    InvalidInputError,
    NotFoundError,
)


@dataclass(eq=False, kw_only=True)
class InventoryItemNotFoundError(NotFoundError):
    inventory_item_id: UUID

    @property
    def message(self) -> str:
        return "Inventory item not found"


@dataclass(eq=False, kw_only=True)
class NotItemOwnerError(AccessDeniedError):
    inventory_item_id: UUID

    @property
    def message(self) -> str:
        return "Only the owner can gift this item"


@dataclass(eq=False, kw_only=True)
class SelfGiftError(InvalidInputError):
    inventory_item_id: UUID

    @property
    def message(self) -> str:
        return "Cannot gift an item to yourself"


@dataclass(frozen=True, kw_only=True)
class InventoryItem:
    """A copy of a catalog item that a player owns."""

    id: UUID
    owner_id: UUID

    item: Item
    obtained_at: datetime

    def gift(
        self,
        *,
        sender_id: UUID,
        receiver_id: UUID,
    ) -> Self:
        if sender_id != self.owner_id:
            raise NotItemOwnerError(inventory_item_id=self.id)

        if receiver_id == self.owner_id:
            raise SelfGiftError(inventory_item_id=self.id)

        return replace(self, owner_id=receiver_id)
