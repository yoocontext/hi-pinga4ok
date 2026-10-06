from uuid import UUID

from sqlalchemy import Row

from application.interfaces.queries.leaderboard import LeaderboardEntry


def leaderboard_entry_from_row(
    *,
    row: Row[tuple[UUID, str, int]],
) -> LeaderboardEntry:
    player_id, nickname, items_count = row

    return LeaderboardEntry(
        player_id=player_id,
        nickname=nickname,
        items_count=items_count,
    )
