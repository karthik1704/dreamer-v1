"""modify

Revision ID: a4e374f735b6
Revises: aed16141d46f
Create Date: 2024-12-09 18:10:05.060186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4e374f735b6'
down_revision: Union[str, None] = 'aed16141d46f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('video_categories_parent_id_fkey', 'video_categories', type_='foreignkey')
    op.create_foreign_key(None, 'video_categories', 'video_categories', ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'video_categories', type_='foreignkey')
    op.create_foreign_key('video_categories_parent_id_fkey', 'video_categories', 'note_categories', ['parent_id'], ['id'])
    # ### end Alembic commands ###
