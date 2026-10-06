from typing import Protocol
from uuid import UUID

from application.entities.case import Case


class ICaseDm(Protocol):
    async def get(
        self,
        *,
        id: UUID,
    ) -> Case | None: ...
