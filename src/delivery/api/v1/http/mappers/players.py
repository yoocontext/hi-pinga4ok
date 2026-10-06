from application.entities.player import Player
from application.use_cases.players.create import CreatePlayerCm
from delivery.api.v1.http.schemas.players import (
    CreatePlayerRequest,
    PlayerResponse,
)


def create_player_command(
    *,
    body: CreatePlayerRequest,
) -> CreatePlayerCm:
    return CreatePlayerCm(nickname=body.nickname)


def player_response(
    *,
    player: Player,
) -> PlayerResponse:
    return PlayerResponse(
        id=player.id,
        nickname=player.nickname,
        balance=player.balance,
        last_bonus_at=player.last_bonus_at,
    )
