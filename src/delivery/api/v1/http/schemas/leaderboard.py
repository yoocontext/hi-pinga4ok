from uuid import UUID

from pydantic import BaseModel


class LeaderboardEntryResponse(BaseModel):
    player_id: UUID
    nickname: str
    items_count: int
