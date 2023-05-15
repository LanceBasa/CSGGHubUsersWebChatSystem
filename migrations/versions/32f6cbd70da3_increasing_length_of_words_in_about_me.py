"""Increasing length of words in about_me

Revision ID: 32f6cbd70da3
Revises: 7a3589291cc4
Create Date: 2023-05-15 18:49:26.981735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32f6cbd70da3'
down_revision = '7a3589291cc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('about_me',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=300),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('about_me',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=140),
               existing_nullable=True)

    # ### end Alembic commands ###
