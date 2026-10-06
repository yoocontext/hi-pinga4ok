from dataclasses import dataclass
from uuid import UUID

from application.entities.player import (
    Player,
    PlayerNotFoundError,
)
from application.interfaces.dm.player import IPlayerDm
from application.use_cases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True)
class GetPlayerCm:
    player_id: UUID


@dataclass(frozen=True, kw_only=True)
class GetPlayerRs:
    player: Player


@dataclass
class GetPlayerUc(BaseUseCase[GetPlayerCm, GetPlayerRs]):
    _player_dm: IPlayerDm

    async def act(
        self,
        *,
        command: GetPlayerCm,
    ) -> GetPlayerRs:
        player = await self._player_dm.get(id=command.player_id)

        if player is None:
            raise PlayerNotFoundError(player_id=command.player_id)

        return GetPlayerRs(player=player)
