"""create userpofile (recovered)

Revision ID: f6994e041d96
Revises: 10277def84d7
Create Date: 2025-03-25 17:50:30.664598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf88ad60e0f5'
down_revision: Union[str, None] = '10277def84d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('userprofile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.Integer(), nullable=False),
        sa.Column('password', sa.Integer(), nullable=False),
        sa.Column('access_token', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('userprofile')
