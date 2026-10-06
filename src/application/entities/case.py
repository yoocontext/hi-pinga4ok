from bisect import bisect_right
from dataclasses import dataclass
from itertools import accumulate
from uuid import UUID

from application.entities.item import Item
from application.exceptions import (
    InvalidStateError,
    NotFoundError,
)


@dataclass(eq=False, kw_only=True)
class CaseNotFoundError(NotFoundError):
    case_id: UUID

    @property
    def message(self) -> str:
        return "Case not found"


@dataclass(eq=False, kw_only=True)
class EmptyCaseError(InvalidStateError):
    case_id: UUID

    @property
    def message(self) -> str:
        return "Case has no drops"


@dataclass(frozen=True, kw_only=True)
class CaseDrop:
    item: Item
    weight: int


@dataclass(frozen=True, kw_only=True)
class Case:
    id: UUID
    name: str
    price: int

    drops: tuple[CaseDrop, ...]

    def __post_init__(self) -> None:
        if not self.drops:
            raise EmptyCaseError(case_id=self.id)

    def roll(
        self,
        *,
        value: float,
    ) -> Item:
        """Pick a drop by weight; `value` is a random number in [0, 1)."""

        # running totals: weights 70, 25, 5 → bounds 70, 95, 100
        bounds = list(accumulate(drop.weight for drop in self.drops))

        index = bisect_right(bounds, value * bounds[-1])

        return self.drops[index].item
