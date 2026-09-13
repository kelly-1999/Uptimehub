"""add monitor status fields

Revision ID: 145325090a4f
Revises: 4f8428f2e5a5
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "145325090a4f"
down_revision: Union[str, Sequence[str], None] = "4f8428f2e5a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "monitors",
        sa.Column(
            "current_status",
            sa.String(length=20),
            nullable=False,
            server_default="unknown",
        ),
    )

    op.add_column(
        "monitors",
        sa.Column(
            "last_http_status",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "monitors",
        sa.Column(
            "last_response_time_ms",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "monitors",
        sa.Column(
            "last_checked_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("monitors", "last_checked_at")
    op.drop_column("monitors", "last_response_time_ms")
    op.drop_column("monitors", "last_http_status")
    op.drop_column("monitors", "current_status")
