"""change Managers

Revision ID: eeae6bb9eac5
Revises: 8db4e1e6c5d6
Create Date: 2022-06-26 18:23:35.444361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeae6bb9eac5'
down_revision = '8db4e1e6c5d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Customers', 'AM_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Customers', 'Addr_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Customers', 'PayTerm_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Managers', 'Sales_Grp',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Managers', 'STL_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Managers', 'LoB_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index('Managers_LoB_id_idx', table_name='Managers')
    op.drop_constraint('Managers_Sales_Grp_key', 'Managers', type_='unique')
    op.create_index(op.f('ix_Managers_LoB_id'), 'Managers', ['LoB_id'], unique=False)
    op.create_index(op.f('ix_Managers_Sales_Grp'), 'Managers', ['Sales_Grp'], unique=True)
    op.drop_constraint('Managers_LoB_id_fkey', 'Managers', type_='foreignkey')
    op.drop_constraint('Managers_STL_id_fkey', 'Managers', type_='foreignkey')
    op.create_foreign_key(None, 'Managers', 'STLs', ['STL_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'Managers', 'LoB', ['LoB_id'], ['id'], ondelete='SET NULL')
    op.alter_column('Shipto', 'SoldTo_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Shipto', 'YFRP_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Shipto', 'AM_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Shipto', 'Addr_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_Shipto_SoldTo_id'), 'Shipto', ['SoldTo_id'], unique=False)
    op.create_index(op.f('ix_Shipto_YFRP_id'), 'Shipto', ['YFRP_id'], unique=False)
    op.alter_column('YFRP', 'Addr_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('YFRP', 'Addr_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index(op.f('ix_Shipto_YFRP_id'), table_name='Shipto')
    op.drop_index(op.f('ix_Shipto_SoldTo_id'), table_name='Shipto')
    op.alter_column('Shipto', 'Addr_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Shipto', 'AM_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Shipto', 'YFRP_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Shipto', 'SoldTo_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'Managers', type_='foreignkey')
    op.drop_constraint(None, 'Managers', type_='foreignkey')
    op.create_foreign_key('Managers_STL_id_fkey', 'Managers', 'STLs', ['STL_id'], ['id'])
    op.create_foreign_key('Managers_LoB_id_fkey', 'Managers', 'LoB', ['LoB_id'], ['id'])
    op.drop_index(op.f('ix_Managers_Sales_Grp'), table_name='Managers')
    op.drop_index(op.f('ix_Managers_LoB_id'), table_name='Managers')
    op.create_unique_constraint('Managers_Sales_Grp_key', 'Managers', ['Sales_Grp'])
    op.create_index('Managers_LoB_id_idx', 'Managers', ['LoB_id'], unique=False)
    op.alter_column('Managers', 'LoB_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Managers', 'STL_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Managers', 'Sales_Grp',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Customers', 'PayTerm_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Customers', 'Addr_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Customers', 'AM_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
