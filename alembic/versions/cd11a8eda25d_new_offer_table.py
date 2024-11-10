"""new_offer_table

Revision ID: cd11a8eda25d
Revises: d95e521cefb1
Create Date: 2024-11-10 12:47:59.391302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd11a8eda25d'
down_revision: Union[str, None] = 'd95e521cefb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sellers_offer',
        sa.Column('uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('seller_uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('product_uuid', sa.CHAR(length=36), nullable=False),
        sa.Column('similarity_score', sa.FLOAT(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_update', sa.DateTime(), nullable=True),
        sa.Column('first_price', sa.FLOAT(), nullable=True),
        sa.Column('last_price', sa.FLOAT(), nullable=True),
        sa.Column('first_stock', sa.INTEGER(), nullable=True),
        sa.Column('last_stock', sa.INTEGER(), nullable=True),
        sa.Column('version', sa.INTEGER(), nullable=True),
        sa.Column('status', sa.VARCHAR(length=10), nullable=False),
        sa.Column('raw_record', sa.TEXT(), nullable=True),
        
        # Llave primaria
        sa.PrimaryKeyConstraint('uuid'),
        
        # Llaves foráneas (si aplican)
        sa.ForeignKeyConstraint(['seller_uuid'], ['sellers.uuid']),
        sa.ForeignKeyConstraint(['product_uuid'], ['catalogue.uuid']),

        # Motor específico de MySQL
        mysql_engine='InnoDB'
    )


def downgrade() -> None:
    op.drop_table('sellers_offer')
