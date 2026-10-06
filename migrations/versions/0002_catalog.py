"""catalog: items and cases to open

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-06
"""

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | None = None
depends_on: str | None = None

items = sa.table(
    "items",
    sa.column("id", sa.Uuid()),
    sa.column("name", sa.String()),
    sa.column("rarity", sa.String()),
)
cases = sa.table(
    "cases",
    sa.column("id", sa.Uuid()),
    sa.column("name", sa.String()),
    sa.column("price", sa.Integer()),
)
case_drops = sa.table(
    "case_drops",
    sa.column("id", sa.Uuid()),
    sa.column("case_id", sa.Uuid()),
    sa.column("item_id", sa.Uuid()),
    sa.column("weight", sa.Integer()),
)

# fixed ids keep the catalog the same on every machine
WOODEN_SWORD = "019a0000-0000-7000-8000-000000000101"
RUSTY_DAGGER = "019a0000-0000-7000-8000-000000000102"
LEATHER_SHIELD = "019a0000-0000-7000-8000-000000000103"
STEEL_AXE = "019a0000-0000-7000-8000-000000000104"
HUNTER_BOW = "019a0000-0000-7000-8000-000000000105"
FROST_STAFF = "019a0000-0000-7000-8000-000000000106"
SHADOW_CLOAK = "019a0000-0000-7000-8000-000000000107"
DRAGON_BLADE = "019a0000-0000-7000-8000-000000000108"

STARTER_CASE = "019a0000-0000-7000-8000-000000000201"
DRAGON_CASE = "019a0000-0000-7000-8000-000000000202"

# weights sum to 100 in each case, so a weight reads as a percent
DROPS = [
    (STARTER_CASE, WOODEN_SWORD, 35),
    (STARTER_CASE, RUSTY_DAGGER, 25),
    (STARTER_CASE, LEATHER_SHIELD, 20),
    (STARTER_CASE, STEEL_AXE, 12),
    (STARTER_CASE, HUNTER_BOW, 6),
    (STARTER_CASE, FROST_STAFF, 2),
    (DRAGON_CASE, STEEL_AXE, 30),
    (DRAGON_CASE, HUNTER_BOW, 25),
    (DRAGON_CASE, FROST_STAFF, 20),
    (DRAGON_CASE, SHADOW_CLOAK, 17),
    (DRAGON_CASE, DRAGON_BLADE, 8),
]


def upgrade() -> None:
    op.bulk_insert(
        items,
        [
            {
                "id": WOODEN_SWORD,
                "name": "Wooden Sword",
                "rarity": "common",
            },
            {
                "id": RUSTY_DAGGER,
                "name": "Rusty Dagger",
                "rarity": "common",
            },
            {
                "id": LEATHER_SHIELD,
                "name": "Leather Shield",
                "rarity": "common",
            },
            {
                "id": STEEL_AXE,
                "name": "Steel Axe",
                "rarity": "rare",
            },
            {
                "id": HUNTER_BOW,
                "name": "Hunter Bow",
                "rarity": "rare",
            },
            {
                "id": FROST_STAFF,
                "name": "Frost Staff",
                "rarity": "epic",
            },
            {
                "id": SHADOW_CLOAK,
                "name": "Shadow Cloak",
                "rarity": "epic",
            },
            {
                "id": DRAGON_BLADE,
                "name": "Dragon Blade",
                "rarity": "legendary",
            },
        ],
    )

    op.bulk_insert(
        cases,
        [
            {
                "id": STARTER_CASE,
                "name": "Starter Case",
                "price": 50,
            },
            {
                "id": DRAGON_CASE,
                "name": "Dragon Case",
                "price": 250,
            },
        ],
    )

    op.bulk_insert(
        case_drops,
        [
            {
                "id": f"019a0000-0000-7000-8000-{index:012d}",
                "case_id": case_id,
                "item_id": item_id,
                "weight": weight,
            }
            for index, (case_id, item_id, weight) in enumerate(DROPS, 301)
        ],
    )


def downgrade() -> None:
    op.execute(case_drops.delete())
    op.execute(cases.delete())
    op.execute(items.delete())
