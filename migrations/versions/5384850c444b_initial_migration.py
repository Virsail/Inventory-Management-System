"""Initial Migration

Revision ID: 5384850c444b
Revises: bbb27131c59e
Create Date: 2020-09-30 17:48:55.571405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5384850c444b'
down_revision = 'bbb27131c59e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_clerks_email', table_name='clerks')
    op.drop_table('clerks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clerks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('id_number', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('profile_pic_path', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('pass_secure', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='clerks_pkey')
    )
    op.create_index('ix_clerks_email', 'clerks', ['email'], unique=True)
    # ### end Alembic commands ###