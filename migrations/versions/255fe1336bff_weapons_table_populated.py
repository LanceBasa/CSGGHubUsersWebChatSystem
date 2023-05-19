"""weapons table populated

Revision ID: 255fe1336bff
Revises: c30d54cfe189
Create Date: 2023-05-19 16:53:30.436902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255fe1336bff'
down_revision = 'c30d54cfe189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('command_name', sa.String(length=64), nullable=True),
    sa.Column('query_command', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('command_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commands')
    # ### end Alembic commands ###
