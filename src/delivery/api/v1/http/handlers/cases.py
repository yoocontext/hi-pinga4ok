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

from application.use_cases.cases.list import ListCasesUc
from application.use_cases.cases.open import (
    OpenCaseCm,
    OpenCaseUc,
)
from delivery.api.v1.http.auth import current_player_id
from delivery.api.v1.http.mappers.cases import (
    case_response,
    open_case_response,
)
from delivery.api.v1.http.schemas.cases import (
    CaseResponse,
    OpenCaseResponse,
)

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
)


@router.get("")
@inject
async def list_cases(
    *,
    use_case: FromDishka[ListCasesUc],
) -> list[CaseResponse]:
    result = await use_case.act(command=None)

    return [case_response(case=case) for case in result.cases]


@router.post("/{case_id}/open")
@inject
async def open_case(
    *,
    case_id: UUID,
    player_id: Annotated[UUID, Depends(current_player_id)],
    use_case: FromDishka[OpenCaseUc],
) -> OpenCaseResponse:
    result = await use_case.act(
        command=OpenCaseCm(
            player_id=player_id,
            case_id=case_id,
        ),
    )

    return open_case_response(result=result)
