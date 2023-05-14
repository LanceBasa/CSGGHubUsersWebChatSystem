"""weapons update

Revision ID: 41931f68745a
Revises: d9b22c88a76d
Create Date: 2023-05-14 14:09:52.735759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41931f68745a'
down_revision = 'd9b22c88a76d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weapon', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weapon', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('category')

    # ### end Alembic commands ###
