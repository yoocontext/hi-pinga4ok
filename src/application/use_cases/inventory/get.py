from dataclasses import dataclass
from uuid import UUID

from application.entities.inventory_item import InventoryItem
from application.entities.player import PlayerNotFoundError
from application.interfaces.dm.player import IPlayerDm
from application.interfaces.queries.inventory import IInventoryQueries
from application.use_cases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True)
class GetInventoryCm:
    player_id: UUID


@dataclass(frozen=True, kw_only=True)
class GetInventoryRs:
    items: tuple[InventoryItem, ...]


@dataclass
class GetInventoryUc(BaseUseCase[GetInventoryCm, GetInventoryRs]):
    _player_dm: IPlayerDm
    _inventory_queries: IInventoryQueries

    async def act(
        self,
        *,
        command: GetInventoryCm,
    ) -> GetInventoryRs:
        # an unknown player must be 404, not an empty inventory
        if await self._player_dm.get(id=command.player_id) is None:
            raise PlayerNotFoundError(player_id=command.player_id)

        items = await self._inventory_queries.items(owner_id=command.player_id)

        return GetInventoryRs(items=tuple(items))
