"""Alterando tipos de colunas

Revision ID: 3be558576e38
Revises: 937a08a27fe8
Create Date: 2025-08-22 12:31:25.968657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3be558576e38'
down_revision: Union[str, None] = '937a08a27fe8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Se quiser apenas setar defaults no banco, mantendo NOT NULL:
    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),              # tinyint(1)
        server_default=sa.text("1"),             # default 1 (true) no MySQL
        existing_nullable=False,
    )

    op.alter_column(
        "users",
        "balance",
        existing_type=sa.Float(),
        server_default=sa.text("0"),             # default 0.0
        existing_nullable=False,
    )

    # ENUM precisa de aspas simples no literal de default
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("USER", "ADMIN", name="role"),  # nome do tipo pode variar
        server_default=sa.text("'USER'"),
        existing_nullable=False,
    )

def downgrade() -> None:
    """Downgrade schema."""
    
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("USER", "ADMIN", name="role"),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "balance",
        existing_type=sa.Float(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),
        server_default=None,
        existing_nullable=False,
    )
