"""posts table

Revision ID: 7eff78fc31cb
Revises: ffee4788a2ac
Create Date: 2023-05-12 16:30:40.149729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eff78fc31cb'
down_revision = 'ffee4788a2ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    # ### end Alembic commands ###
