"""create users table

Revision ID: fc82058b03b5
Revises: 
Create Date: 2026-03-06 14:23:10.117177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'fc82058b03b5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('public_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('public_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
