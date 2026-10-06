from dataclasses import dataclass
from uuid import UUID

from application.entities.inventory_item import (
    InventoryItem,
    InventoryItemNotFoundError,
)
from application.entities.player import PlayerNotFoundError
from application.interfaces.dm.inventory_item import IInventoryItemDm
from application.interfaces.dm.player import IPlayerDm
from application.interfaces.transaction_manager import ITransactionManager
from application.use_cases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True)
class GiftItemCm:
    sender_id: UUID
    receiver_id: UUID
    inventory_item_id: UUID


@dataclass(frozen=True, kw_only=True)
class GiftItemRs:
    inventory_item: InventoryItem


@dataclass
class GiftItemUc(BaseUseCase[GiftItemCm, GiftItemRs]):
    _inventory_item_dm: IInventoryItemDm
    _player_dm: IPlayerDm
    _transaction_manager: ITransactionManager

    async def act(
        self,
        *,
        command: GiftItemCm,
    ) -> GiftItemRs:
        # lock the item so it cannot be gifted to two players at once
        inventory_item = await self._lock_item(id=command.inventory_item_id)

        inventory_item = inventory_item.gift(
            sender_id=command.sender_id,
            receiver_id=command.receiver_id,
        )

        await self._ensure_player_exists(player_id=command.receiver_id)

        await self._inventory_item_dm.save(entity=inventory_item)

        await self._transaction_manager.commit()

        return GiftItemRs(inventory_item=inventory_item)

    async def _lock_item(
        self,
        *,
        id: UUID,
    ) -> InventoryItem:
        inventory_item = await self._inventory_item_dm.get_for_update(id=id)

        if inventory_item is None:
            raise InventoryItemNotFoundError(inventory_item_id=id)

        return inventory_item

    async def _ensure_player_exists(
        self,
        *,
        player_id: UUID,
    ) -> None:
        if await self._player_dm.get(id=player_id) is None:
            raise PlayerNotFoundError(player_id=player_id)
