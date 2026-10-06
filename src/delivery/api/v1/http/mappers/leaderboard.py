from application.interfaces.queries.leaderboard import LeaderboardEntry
from delivery.api.v1.http.schemas.leaderboard import LeaderboardEntryResponse


def leaderboard_entry_response(
    *,
    entry: LeaderboardEntry,
) -> LeaderboardEntryResponse:
    return LeaderboardEntryResponse(
        player_id=entry.player_id,
        nickname=entry.nickname,
        items_count=entry.items_count,
    )
