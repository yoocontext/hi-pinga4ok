from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.use_cases.players.claim_daily_bonus import (
    ClaimDailyBonusCm,
    ClaimDailyBonusUc,
)
from application.use_cases.players.create import CreatePlayerUc
from application.use_cases.players.get import (
    GetPlayerCm,
    GetPlayerUc,
)
from delivery.api.v1.http.auth import current_player_id
from delivery.api.v1.http.mappers.players import (
    create_player_command,
    player_response,
)
from delivery.api.v1.http.schemas.players import (
    CreatePlayerRequest,
    PlayerResponse,
)

router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_player(
    *,
    body: CreatePlayerRequest,
    use_case: FromDishka[CreatePlayerUc],
) -> PlayerResponse:
    result = await use_case.act(command=create_player_command(body=body))

    return player_response(player=result.player)


@router.post("/me/daily-bonus")
@inject
async def claim_daily_bonus(
    *,
    player_id: Annotated[UUID, Depends(current_player_id)],
    use_case: FromDishka[ClaimDailyBonusUc],
) -> PlayerResponse:
    result = await use_case.act(command=ClaimDailyBonusCm(player_id=player_id))

    return player_response(player=result.player)


@router.get("/{player_id}")
@inject
async def get_player(
    *,
    player_id: UUID,
    use_case: FromDishka[GetPlayerUc],
) -> PlayerResponse:
    result = await use_case.act(command=GetPlayerCm(player_id=player_id))

    return player_response(player=result.player)
