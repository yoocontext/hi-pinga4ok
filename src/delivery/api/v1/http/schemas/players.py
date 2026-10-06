from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)


class CreatePlayerRequest(BaseModel):
    nickname: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^\w+$",
    )


class PlayerResponse(BaseModel):
    id: UUID
    nickname: str
    balance: int
    last_bonus_at: datetime | None
