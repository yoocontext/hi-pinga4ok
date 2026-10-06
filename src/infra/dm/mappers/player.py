from application.entities.player import Player
from infra.orm.players import PlayerOrm


def player_from_orm(
    *,
    orm: PlayerOrm,
) -> Player:
    return Player(
        id=orm.id,
        nickname=orm.nickname,
        balance=orm.balance,
        last_bonus_at=orm.last_bonus_at,
    )


def player_to_orm(
    *,
    entity: Player,
) -> PlayerOrm:
    return PlayerOrm(
        id=entity.id,
        nickname=entity.nickname,
        balance=entity.balance,
        last_bonus_at=entity.last_bonus_at,
    )
