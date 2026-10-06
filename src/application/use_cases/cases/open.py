from dataclasses import dataclass
from uuid import (
    UUID,
    uuid7,
)

from application.entities.case import (
    Case,
    CaseNotFoundError,
)
from application.entities.inventory_item import InventoryItem
from application.entities.player import (
    Player,
    PlayerNotFoundError,
)
from application.interfaces.clock import IClock
from application.interfaces.dm.case import ICaseDm
from application.interfaces.dm.inventory_item import IInventoryItemDm
from application.interfaces.dm.player import IPlayerDm
from application.interfaces.random import IRandom
from application.interfaces.transaction_manager import ITransactionManager
from application.use_cases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True)
class OpenCaseCm:
    player_id: UUID
    case_id: UUID


@dataclass(frozen=True, kw_only=True)
class OpenCaseRs:
    inventory_item: InventoryItem
    balance: int


@dataclass
class OpenCaseUc(BaseUseCase[OpenCaseCm, OpenCaseRs]):
    _player_dm: IPlayerDm
    _case_dm: ICaseDm
    _inventory_item_dm: IInventoryItemDm
    _transaction_manager: ITransactionManager
    _random: IRandom
    _clock: IClock

    async def act(
        self,
        *,
        command: OpenCaseCm,
    ) -> OpenCaseRs:
        # lock the player so parallel openings cannot spend the same coins
        player = await self._lock_player(player_id=command.player_id)
        case = await self._get_case(case_id=command.case_id)

        player = player.spend(amount=case.price)

        inventory_item = self._drop_item(
            player=player,
            case=case,
        )

        await self._player_dm.save(entity=player)
        self._inventory_item_dm.add(entity=inventory_item)

        await self._transaction_manager.commit()

        return OpenCaseRs(
            inventory_item=inventory_item,
            balance=player.balance,
        )

    async def _lock_player(
        self,
        *,
        player_id: UUID,
    ) -> Player:
        player = await self._player_dm.get_for_update(id=player_id)

        if player is None:
            raise PlayerNotFoundError(player_id=player_id)

        return player

    async def _get_case(
        self,
        *,
        case_id: UUID,
    ) -> Case:
        case = await self._case_dm.get(id=case_id)

        if case is None:
            raise CaseNotFoundError(case_id=case_id)

        return case

    def _drop_item(
        self,
        *,
        player: Player,
        case: Case,
    ) -> InventoryItem:
        return InventoryItem(
            id=uuid7(),
            owner_id=player.id,
            item=case.roll(value=self._random.value()),
            obtained_at=self._clock.now(),
        )
