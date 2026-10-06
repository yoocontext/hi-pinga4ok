from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

CmT = TypeVar("CmT")
RsT = TypeVar("RsT")


class BaseUseCase(
    ABC,
    Generic[CmT, RsT],
):
    @abstractmethod
    async def act(
        self,
        *,
        command: CmT,
    ) -> RsT:
        raise NotImplementedError
