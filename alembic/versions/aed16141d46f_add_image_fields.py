"""add image fields

Revision ID: aed16141d46f
Revises: 0fcd3d25c8eb
Create Date: 2024-12-09 12:50:37.557020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aed16141d46f'
down_revision: Union[str, None] = '0fcd3d25c8eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note_categories', sa.Column('image', sa.Text(), nullable=True))
    op.add_column('video_categories', sa.Column('image', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video_categories', 'image')
    op.drop_column('note_categories', 'image')
    # ### end Alembic commands ###
