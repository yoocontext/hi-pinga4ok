from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)

from application.use_cases.inventory.get import (
    GetInventoryCm,
    GetInventoryUc,
)
from application.use_cases.inventory.gift import GiftItemUc
from delivery.api.v1.http.auth import current_player_id
from delivery.api.v1.http.mappers.inventory import (
    gift_item_command,
    inventory_item_response,
)
from delivery.api.v1.http.schemas.inventory import (
    GiftItemRequest,
    InventoryItemResponse,
)

router = APIRouter(tags=["inventory"])


@router.get("/players/{player_id}/inventory")
@inject
async def get_inventory(
    *,
    player_id: UUID,
    use_case: FromDishka[GetInventoryUc],
) -> list[InventoryItemResponse]:
    result = await use_case.act(command=GetInventoryCm(player_id=player_id))

    return [
        inventory_item_response(inventory_item=inventory_item)
        for inventory_item in result.items
    ]


@router.post("/inventory/{inventory_item_id}/gift")
@inject
async def gift_item(
    *,
    inventory_item_id: UUID,
    body: GiftItemRequest,
    player_id: Annotated[UUID, Depends(current_player_id)],
    use_case: FromDishka[GiftItemUc],
) -> InventoryItemResponse:
    result = await use_case.act(
        command=gift_item_command(
            body=body,
            sender_id=player_id,
            inventory_item_id=inventory_item_id,
        ),
    )

    return inventory_item_response(inventory_item=result.inventory_item)
