from fastapi import APIRouter

from delivery.api.v1.http.handlers import (
    cases,
    inventory,
    leaderboard,
    players,
)

router = APIRouter(prefix="/api/v1")
router.include_router(players.router)
router.include_router(cases.router)
router.include_router(inventory.router)
router.include_router(leaderboard.router)
