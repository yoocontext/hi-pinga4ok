from uuid import UUID

from application.entities.inventory_item import InventoryItem
from application.use_cases.inventory.gift import GiftItemCm
from delivery.api.v1.http.mappers.cases import item_response
from delivery.api.v1.http.schemas.inventory import (
    GiftItemRequest,
    InventoryItemResponse,
)


def gift_item_command(
    *,
    body: GiftItemRequest,
    sender_id: UUID,
    inventory_item_id: UUID,
) -> GiftItemCm:
    return GiftItemCm(
        sender_id=sender_id,
        receiver_id=body.receiver_id,
        inventory_item_id=inventory_item_id,
    )


def inventory_item_response(
    *,
    inventory_item: InventoryItem,
) -> InventoryItemResponse:
    return InventoryItemResponse(
        id=inventory_item.id,
        owner_id=inventory_item.owner_id,
        item=item_response(item=inventory_item.item),
        obtained_at=inventory_item.obtained_at,
    )
