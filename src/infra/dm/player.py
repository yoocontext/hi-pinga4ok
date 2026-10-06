from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.entities.player import Player
from infra.dm.mappers.player import (
    player_from_orm,
    player_to_orm,
)
from infra.orm.players import PlayerOrm


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyPlayerDm:
    session: AsyncSession

    async def get(
        self,
        *,
        id: UUID,
    ) -> Player | None:
        orm = await self.session.get(PlayerOrm, id)

        return None if orm is None else player_from_orm(orm=orm)

    async def get_for_update(
        self,
        *,
        id: UUID,
    ) -> Player | None:
        stmt = (
            select(PlayerOrm)
            .where(PlayerOrm.id == id)
            .with_for_update()
            # the row may already sit in the session; re-read it after the lock
            .execution_options(populate_existing=True)
        )

        orm = await self.session.scalar(stmt)

        return None if orm is None else player_from_orm(orm=orm)

    def add(
        self,
        *,
        entity: Player,
    ) -> None:
        self.session.add(player_to_orm(entity=entity))

    async def save(
        self,
        *,
        entity: Player,
    ) -> None:
        await self.session.merge(player_to_orm(entity=entity))
