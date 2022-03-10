"""Updated posts

Revision ID: 1495a9baf5ec
Revises: 5b7f6e29587e
Create Date: 2022-03-01 11:09:25.470485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1495a9baf5ec'
down_revision = '5b7f6e29587e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
