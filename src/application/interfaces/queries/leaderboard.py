from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class LeaderboardEntry:
    player_id: UUID
    nickname: str
    items_count: int


class ILeaderboardQueries(Protocol):
    async def top(
        self,
        *,
        limit: int,
    ) -> list[LeaderboardEntry]:
        """Return players with the most items first."""
        ...
