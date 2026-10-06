"""schema

Revision ID: 0001
Revises:
Create Date: 2026-10-06
"""

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nickname", sa.String(length=32), nullable=False),
        sa.Column("balance", sa.Integer(), nullable=False),
        sa.Column("last_bonus_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "balance >= 0",
            name=op.f("ck_players_balance_not_negative"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_players")),
        sa.UniqueConstraint("nickname", name=op.f("uq_players_nickname")),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("rarity", sa.String(length=16), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_items")),
    )

    op.create_table(
        "cases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.CheckConstraint("price > 0", name=op.f("ck_cases_price_positive")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cases")),
    )

    op.create_table(
        "case_drops",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "weight > 0",
            name=op.f("ck_case_drops_weight_positive"),
        ),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["cases.id"],
            name=op.f("fk_case_drops_case_id_cases"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
            name=op.f("fk_case_drops_item_id_items"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_case_drops")),
    )

    op.create_index(
        op.f("ix_case_drops_case_id"),
        "case_drops",
        ["case_id"],
    )

    op.create_table(
        "inventory_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("obtained_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["players.id"],
            name=op.f("fk_inventory_items_owner_id_players"),
        ),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
            name=op.f("fk_inventory_items_item_id_items"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_inventory_items")),
    )

    op.create_index(
        op.f("ix_inventory_items_owner_id"),
        "inventory_items",
        ["owner_id"],
    )


def downgrade() -> None:
    op.drop_table("inventory_items")
    op.drop_table("case_drops")
    op.drop_table("cases")
    op.drop_table("items")
    op.drop_table("players")
