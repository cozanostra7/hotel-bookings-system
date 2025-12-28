"""check if the user exists

Revision ID: d8a82d6b81e8
Revises: ca605a8d6e0a
Create Date: 2025-12-28 20:26:18.108074

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "d8a82d6b81e8"
down_revision: Union[str, Sequence[str], None] = "ca605a8d6e0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=200),
        existing_nullable=False,
    )
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:

    op.drop_constraint(None, "users", type_="unique")
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )

