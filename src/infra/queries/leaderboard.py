from dataclasses import dataclass

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.queries.leaderboard import LeaderboardEntry
from infra.orm.inventory import InventoryItemOrm
from infra.orm.players import PlayerOrm
from infra.queries.mappers.leaderboard import leaderboard_entry_from_row


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyLeaderboardQueries:
    session: AsyncSession

    async def top(
        self,
        *,
        limit: int,
    ) -> list[LeaderboardEntry]:
        items_count = func.count(InventoryItemOrm.id)

        # outer join keeps players who have not opened a case yet
        stmt = (
            select(PlayerOrm.id, PlayerOrm.nickname, items_count)
            .outerjoin(
                InventoryItemOrm,
                InventoryItemOrm.owner_id == PlayerOrm.id,
            )
            .group_by(PlayerOrm.id)
            .order_by(items_count.desc(), PlayerOrm.nickname)
            .limit(limit)
        )

        rows = await self.session.execute(stmt)

        return [leaderboard_entry_from_row(row=row) for row in rows]
