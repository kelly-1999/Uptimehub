"""use timezone aware timestamps

Revision ID: 39f15e7748a2
Revises: 145325090a4f
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "39f15e7748a2"
down_revision: Union[str, Sequence[str], None] = "145325090a4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "monitors",
        "last_checked_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="last_checked_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "monitors",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )


def downgrade() -> None:
    op.alter_column(
        "monitors",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "monitors",
        "last_checked_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=True,
        postgresql_using="last_checked_at AT TIME ZONE 'UTC'",
    )
