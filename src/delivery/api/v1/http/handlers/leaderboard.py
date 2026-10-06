from typing import Annotated

from dishka.integrations.fastapi import (
    FromDishka,
    inject,
)
from fastapi import (
    APIRouter,
    Query,
)

from application.use_cases.get_leaderboard import (
    GetLeaderboardCm,
    GetLeaderboardUc,
)
from delivery.api.v1.http.mappers.leaderboard import leaderboard_entry_response
from delivery.api.v1.http.schemas.leaderboard import LeaderboardEntryResponse

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
)


@router.get("")
@inject
async def get_leaderboard(
    *,
    use_case: FromDishka[GetLeaderboardUc],
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
        ),
    ] = 10,
) -> list[LeaderboardEntryResponse]:
    result = await use_case.act(command=GetLeaderboardCm(limit=limit))

    return [leaderboard_entry_response(entry=entry) for entry in result.entries]
