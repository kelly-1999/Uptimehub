"""create monitors table

Revision ID: 4f8428f2e5a5
Revises:
Create Date: 2026-09-13 13:43:33.278156
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4f8428f2e5a5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "monitors",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "url",
            sa.String(length=500),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "interval_seconds",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_monitors_id"),
        "monitors",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_monitors_id"),
        table_name="monitors",
    )

    op.drop_table("monitors")
