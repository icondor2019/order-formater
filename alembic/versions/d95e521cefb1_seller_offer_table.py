"""seller_offer table

Revision ID: d95e521cefb1
Revises: 08b5502bbaed
Create Date: 2024-06-27 19:37:04.212518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd95e521cefb1'
down_revision: Union[str, None] = '08b5502bbaed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('seller_uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('product_uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('raw_description', sa.VARCHAR(length=250), nullable=False),
        sa.Column('stock', sa.INTEGER(), nullable=False),
        sa.Column('price', sa.FLOAT(), nullable=False),
        sa.Column('status', sa.VARCHAR(length=10), nullable=False),
        sa.PrimaryKeyConstraint('uuid'),
        sa.ForeignKeyConstraint(['seller_uuid'], ['sellers.uuid']),
        sa.ForeignKeyConstraint(['product_uuid'], ['catalogue.uuid']),
        mysql_engine='InnoDB'
    )

def downgrade() -> None:
    op.drop_table('products')
