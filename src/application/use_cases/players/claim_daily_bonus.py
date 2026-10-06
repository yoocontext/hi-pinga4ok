from dataclasses import dataclass
from uuid import UUID

from application.entities.player import (
    Player,
    PlayerNotFoundError,
)
from application.interfaces.clock import IClock
from application.interfaces.dm.player import IPlayerDm
from application.interfaces.transaction_manager import ITransactionManager
from application.use_cases.base import BaseUseCase
from application.use_cases.players.config import PlayersConfig


@dataclass(frozen=True, kw_only=True)
class ClaimDailyBonusCm:
    player_id: UUID


@dataclass(frozen=True, kw_only=True)
class ClaimDailyBonusRs:
    player: Player


@dataclass
class ClaimDailyBonusUc(BaseUseCase[ClaimDailyBonusCm, ClaimDailyBonusRs]):
    _player_dm: IPlayerDm
    _transaction_manager: ITransactionManager
    _clock: IClock
    _config: PlayersConfig

    async def act(
        self,
        *,
        command: ClaimDailyBonusCm,
    ) -> ClaimDailyBonusRs:
        # lock the player so a double click cannot claim the bonus twice
        player = await self._player_dm.get_for_update(id=command.player_id)

        if player is None:
            raise PlayerNotFoundError(player_id=command.player_id)

        player = player.claim_daily_bonus(
            amount=self._config.daily_bonus,
            cooldown=self._config.daily_bonus_cooldown,
            at=self._clock.now(),
        )

        await self._player_dm.save(entity=player)

        await self._transaction_manager.commit()

        return ClaimDailyBonusRs(player=player)
