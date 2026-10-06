from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.entities.item import Rarity


class ItemResponse(BaseModel):
    id: UUID
    name: str
    rarity: Rarity


class CaseDropResponse(BaseModel):
    item: ItemResponse
    chance: float


class CaseResponse(BaseModel):
    id: UUID
    name: str
    price: int
    drops: list[CaseDropResponse]


class OpenCaseResponse(BaseModel):
    inventory_item_id: UUID
    item: ItemResponse
    obtained_at: datetime
    balance: int
