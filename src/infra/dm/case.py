from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.entities.case import Case
from infra.dm.mappers.case import (
    case_from_orm,
    case_loading,
)
from infra.orm.cases import CaseOrm


@dataclass(eq=False, repr=False, kw_only=True)
class AlchemyCaseDm:
    session: AsyncSession

    async def get(
        self,
        *,
        id: UUID,
    ) -> Case | None:
        stmt = select(CaseOrm).where(CaseOrm.id == id).options(case_loading())

        orm = await self.session.scalar(stmt)

        return None if orm is None else case_from_orm(orm=orm)
