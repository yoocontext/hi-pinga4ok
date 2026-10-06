from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from delivery.api.v1.http.schemas.cases import ItemResponse


class GiftItemRequest(BaseModel):
    receiver_id: UUID


class InventoryItemResponse(BaseModel):
    id: UUID
    owner_id: UUID
    item: ItemResponse
    obtained_at: datetime
