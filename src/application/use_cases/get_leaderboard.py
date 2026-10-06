from dataclasses import dataclass

from application.interfaces.queries.leaderboard import (
    ILeaderboardQueries,
    LeaderboardEntry,
)
from application.use_cases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True)
class GetLeaderboardCm:
    limit: int


@dataclass(frozen=True, kw_only=True)
class GetLeaderboardRs:
    entries: tuple[LeaderboardEntry, ...]


@dataclass
class GetLeaderboardUc(BaseUseCase[GetLeaderboardCm, GetLeaderboardRs]):
    _leaderboard_queries: ILeaderboardQueries

    async def act(
        self,
        *,
        command: GetLeaderboardCm,
    ) -> GetLeaderboardRs:
        entries = await self._leaderboard_queries.top(limit=command.limit)

        return GetLeaderboardRs(entries=tuple(entries))
