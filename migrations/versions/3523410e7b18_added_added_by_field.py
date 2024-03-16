"""added added_by field

Revision ID: 3523410e7b18
Revises: 
Create Date: 2024-03-16 13:54:39.831562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3523410e7b18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('added_by', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.drop_column('added_by')

    # ### end Alembic commands ###
