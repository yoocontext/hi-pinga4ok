from dataclasses import dataclass

from sqlalchemy import (
    exists,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from infra.orm.players import PlayerOrm


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyPlayersQueries:
    session: AsyncSession

    async def nickname_taken(
        self,
        *,
        nickname: str,
    ) -> bool:
        taken = await self.session.scalar(
            select(exists().where(PlayerOrm.nickname == nickname)),
        )

        return bool(taken)
