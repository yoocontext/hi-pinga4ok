from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.entities.case import Case
from infra.dm.mappers.case import (
    case_from_orm,
    case_loading,
)
from infra.orm.cases import CaseOrm


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyCasesQueries:
    session: AsyncSession

    async def catalog(self) -> list[Case]:
        # 2 queries for any number of cases: cases, then drops joined with
        # items; without case_loading() lazy="raise" fails on `orm.drops`
        stmt = select(CaseOrm).options(case_loading()).order_by(CaseOrm.price)

        orms = await self.session.scalars(stmt)

        return [case_from_orm(orm=orm) for orm in orms]
