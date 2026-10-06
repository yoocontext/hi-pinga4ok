from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class Rarity(StrEnum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass(frozen=True, kw_only=True)
class Item:
    id: UUID
    name: str
    rarity: Rarity
