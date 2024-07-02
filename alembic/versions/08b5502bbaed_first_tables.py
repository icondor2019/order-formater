"""table_sellers

Revision ID: 08b5502bbaed
Revises:
Create Date: 2024-06-22 12:26:24.763104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08b5502bbaed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sellers',
        sa.Column('uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('user_id', sa.CHAR(length=10), nullable=False),
        sa.Column('name', sa.VARCHAR(length=50)),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('status', sa.VARCHAR(length=20)),
        sa.PrimaryKeyConstraint('uuid'),
        mysql_engine='InnoDB'
    )
    op.create_table(
        'catalogue',
        sa.Column('uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('name', sa.VARCHAR(length=50)),
        sa.Column('size', sa.INTEGER(), nullable=False),
        sa.Column('color', sa.VARCHAR(length=25)),
        sa.Column('stems', sa.INTEGER(), nullable=False),
        sa.Column('package', sa.VARCHAR(length=10)),
        sa.Column('description', sa.VARCHAR(length=250)),
        sa.Column('embedding', sa.BLOB()),
        sa.PrimaryKeyConstraint('uuid'),
        mysql_engine='InnoDB'
    )


def downgrade() -> None:
    op.drop_table('sellers')
    op.drop_table('catalogue')
