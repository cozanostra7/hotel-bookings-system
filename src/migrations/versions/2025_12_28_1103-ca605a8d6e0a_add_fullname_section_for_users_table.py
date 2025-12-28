"""add fullname section for users table

Revision ID: ca605a8d6e0a
Revises: e9f1171f3100
Create Date: 2025-12-28 11:03:54.311777

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "ca605a8d6e0a"
down_revision: Union[str, Sequence[str], None] = "e9f1171f3100"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("fullname", sa.String(length=200), nullable=False))



def downgrade() -> None:
    op.drop_column("users", "fullname")

