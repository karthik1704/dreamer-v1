"""add father and mother in student

Revision ID: 29818d71b535
Revises: 4c8273c40efe
Create Date: 2024-11-20 18:37:20.458373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29818d71b535'
down_revision: Union[str, None] = '4c8273c40efe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_profiles', sa.Column('father_name', sa.String(), nullable=True))
    op.add_column('student_profiles', sa.Column('mother_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student_profiles', 'mother_name')
    op.drop_column('student_profiles', 'father_name')
    # ### end Alembic commands ###