from typing import Protocol


class IPlayersQueries(Protocol):
    async def nickname_taken(
        self,
        *,
        nickname: str,
    ) -> bool: ...
