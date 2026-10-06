from typing import Protocol
from uuid import UUID

from application.entities.player import Player


class IPlayerDm(Protocol):
    async def get(
        self,
        *,
        id: UUID,
    ) -> Player | None: ...

    async def get_for_update(
        self,
        *,
        id: UUID,
    ) -> Player | None: ...

    def add(
        self,
        *,
        entity: Player,
    ) -> None: ...

    async def save(
        self,
        *,
        entity: Player,
    ) -> None: ...
