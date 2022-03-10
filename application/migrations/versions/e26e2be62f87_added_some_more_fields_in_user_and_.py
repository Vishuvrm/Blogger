"""Added some more fields in user and updated profile layout in the user dashboard

Revision ID: e26e2be62f87
Revises: 8fa4e8d8505c
Create Date: 2022-03-05 15:34:21.856180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e26e2be62f87'
down_revision = '8fa4e8d8505c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', sa.String(length=25), nullable=True))
    op.add_column('user', sa.Column('profile_image', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('profession', sa.String(length=150), nullable=True))
    op.add_column('user', sa.Column('skills', sa.String(length=500), nullable=True))
    op.add_column('user', sa.Column('about', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'about')
    op.drop_column('user', 'skills')
    op.drop_column('user', 'profession')
    op.drop_column('user', 'profile_image')
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###
