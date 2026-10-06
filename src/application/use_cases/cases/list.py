from dataclasses import dataclass

from application.entities.case import Case
from application.interfaces.queries.cases import ICasesQueries
from application.use_cases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True)
class ListCasesRs:
    cases: tuple[Case, ...]


@dataclass
class ListCasesUc(BaseUseCase[None, ListCasesRs]):
    _cases_queries: ICasesQueries

    async def act(
        self,
        *,
        command: None,
    ) -> ListCasesRs:
        cases = await self._cases_queries.catalog()

        return ListCasesRs(cases=tuple(cases))
