from typing import Protocol

from application.entities.case import Case


class ICasesQueries(Protocol):
    async def catalog(self) -> list[Case]: ...
