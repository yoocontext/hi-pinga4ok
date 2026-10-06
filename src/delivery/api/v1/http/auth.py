from typing import Annotated
from uuid import UUID

from fastapi import Header


async def current_player_id(
    *,
    x_player_id: Annotated[UUID, Header()],
) -> UUID:
    """Stub auth: the client sends its own id in `X-Player-Id`.

    enough for a learning project; a real app verifies a token here.
    """

    return x_player_id
