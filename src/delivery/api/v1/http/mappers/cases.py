from application.entities.case import Case
from application.entities.item import Item
from application.use_cases.cases.open import OpenCaseRs
from delivery.api.v1.http.schemas.cases import (
    CaseDropResponse,
    CaseResponse,
    ItemResponse,
    OpenCaseResponse,
)


def item_response(
    *,
    item: Item,
) -> ItemResponse:
    return ItemResponse(
        id=item.id,
        name=item.name,
        rarity=item.rarity,
    )


def case_response(
    *,
    case: Case,
) -> CaseResponse:
    total_weight = sum(drop.weight for drop in case.drops)

    return CaseResponse(
        id=case.id,
        name=case.name,
        price=case.price,
        drops=[
            CaseDropResponse(
                item=item_response(item=drop.item),
                chance=drop.weight / total_weight,
            )
            for drop in case.drops
        ],
    )


def open_case_response(
    *,
    result: OpenCaseRs,
) -> OpenCaseResponse:
    return OpenCaseResponse(
        inventory_item_id=result.inventory_item.id,
        item=item_response(item=result.inventory_item.item),
        obtained_at=result.inventory_item.obtained_at,
        balance=result.balance,
    )
