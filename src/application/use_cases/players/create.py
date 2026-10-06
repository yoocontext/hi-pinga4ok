from dataclasses import dataclass
from uuid import uuid7

from application.entities.player import Player
from application.exceptions import InvalidStateError
from application.interfaces.dm.player import IPlayerDm
from application.interfaces.queries.players import IPlayersQueries
from application.interfaces.transaction_manager import ITransactionManager
from application.use_cases.base import BaseUseCase
from application.use_cases.players.config import PlayersConfig


@dataclass(eq=False, kw_only=True)
class NicknameTakenError(InvalidStateError):
    nickname: str

    @property
    def message(self) -> str:
        return "Nickname is already taken"


@dataclass(frozen=True, kw_only=True)
class CreatePlayerCm:
    nickname: str


@dataclass(frozen=True, kw_only=True)
class CreatePlayerRs:
    player: Player


@dataclass
class CreatePlayerUc(BaseUseCase[CreatePlayerCm, CreatePlayerRs]):
    _player_dm: IPlayerDm
    _players_queries: IPlayersQueries
    _transaction_manager: ITransactionManager
    _config: PlayersConfig

    async def act(
        self,
        *,
        command: CreatePlayerCm,
    ) -> CreatePlayerRs:
        await self._ensure_nickname_free(nickname=command.nickname)

        player = Player(
            id=uuid7(),
            nickname=command.nickname,
            balance=self._config.start_balance,
        )

        self._player_dm.add(entity=player)

        await self._transaction_manager.commit()

        return CreatePlayerRs(player=player)

    async def _ensure_nickname_free(
        self,
        *,
        nickname: str,
    ) -> None:
        if await self._players_queries.nickname_taken(nickname=nickname):
            raise NicknameTakenError(nickname=nickname)
