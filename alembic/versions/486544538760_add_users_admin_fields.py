"""add users admin fields

Revision ID: 486544538760
Revises: d40a11f03c5d
Create Date: 2024-09-28 20:40:24.601776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '486544538760'
down_revision: Union[str, None] = 'd40a11f03c5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_staff', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_staff')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
