"""Initial Migration

Revision ID: 9cadd47fbccc
Revises: 
Create Date: 2020-09-30 17:53:25.627883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cadd47fbccc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('profile_pic_path', sa.String(), nullable=True),
    sa.Column('role', sa.String(length=255), nullable=True),
    sa.Column('pass_secure', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###