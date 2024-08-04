"""empty message

Revision ID: a81429fd3eaa
Revises: 2e4eca7796fc
Create Date: 2024-08-04 16:24:11.263491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a81429fd3eaa'
down_revision: Union[str, None] = '2e4eca7796fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('time', sa.DateTime(), nullable=True))
    op.alter_column('users', 'days',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'days',
               existing_type=sa.Integer(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.drop_column('users', 'time')
    # ### end Alembic commands ###
