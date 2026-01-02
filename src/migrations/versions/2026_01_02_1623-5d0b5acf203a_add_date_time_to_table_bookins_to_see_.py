"""add date time to table bookins to see when the bookins was doone

Revision ID: 5d0b5acf203a
Revises: c2edf605fbf6
Create Date: 2026-01-02 16:23:22.297518

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5d0b5acf203a"
down_revision: Union[str, Sequence[str], None] = "c2edf605fbf6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )



def downgrade() -> None:
    op.drop_column("bookings", "created_at")

