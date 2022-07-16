"""admin table created

Revision ID: 69c7248c505b
Revises: c0a2fd71c0ea
Create Date: 2022-07-16 09:14:03.952800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69c7248c505b'
down_revision = 'c0a2fd71c0ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('last_visit', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_role'), 'admin', ['role'], unique=False)
    op.create_index(op.f('ix_admin_username'), 'admin', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_username'), table_name='admin')
    op.drop_index(op.f('ix_admin_role'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
