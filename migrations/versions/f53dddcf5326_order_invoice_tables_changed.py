"""Order & Invoice tables changed

Revision ID: f53dddcf5326
Revises: b1c87168d205
Create Date: 2022-07-17 20:58:48.546574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f53dddcf5326'
down_revision = 'b1c87168d205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_InvoiceLines_Invoice_id', table_name='InvoiceLines')
    op.drop_table('InvoiceLines')
    op.drop_index('ix_Invoices_Order_id', table_name='Invoices')
    op.drop_constraint('Invoices_Delivery_id_fkey', 'Invoices', type_='foreignkey')
    op.drop_constraint('Invoices_ShipTo_id_fkey', 'Invoices', type_='foreignkey')
    op.drop_constraint('Invoices_SoldTo_id_fkey', 'Invoices', type_='foreignkey')
    op.drop_constraint('Invoices_Plant_id_fkey', 'Invoices', type_='foreignkey')
    op.drop_constraint('Invoices_Order_id_fkey', 'Invoices', type_='foreignkey')
    op.drop_column('Invoices', 'SoldTo_id')
    op.drop_column('Invoices', 'ShipTo_id')
    op.drop_column('Invoices', 'Delivery_id')
    op.drop_column('Invoices', 'Plant_id')
    op.drop_column('Invoices', 'Order_id')
    op.add_column('open_order_lines', sa.Column('Delivry_id', sa.Integer(), nullable=True))
    op.add_column('open_order_lines', sa.Column('Invoice_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_open_order_lines_Delivry_id'), 'open_order_lines', ['Delivry_id'], unique=False)
    op.create_index(op.f('ix_open_order_lines_Invoice_id'), 'open_order_lines', ['Invoice_id'], unique=False)
    op.create_foreign_key(None, 'open_order_lines', 'Deliveries', ['Delivry_id'], ['id'])
    op.create_foreign_key(None, 'open_order_lines', 'Invoices', ['Invoice_id'], ['id'])
    op.drop_column('open_order_lines', 'OrderQty')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('open_order_lines', sa.Column('OrderQty', sa.NUMERIC(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'open_order_lines', type_='foreignkey')
    op.drop_constraint(None, 'open_order_lines', type_='foreignkey')
    op.drop_index(op.f('ix_open_order_lines_Invoice_id'), table_name='open_order_lines')
    op.drop_index(op.f('ix_open_order_lines_Delivry_id'), table_name='open_order_lines')
    op.drop_column('open_order_lines', 'Invoice_id')
    op.drop_column('open_order_lines', 'Delivry_id')
    op.add_column('Invoices', sa.Column('Order_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Invoices', sa.Column('Plant_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Invoices', sa.Column('Delivery_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Invoices', sa.Column('ShipTo_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Invoices', sa.Column('SoldTo_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Invoices_Order_id_fkey', 'Invoices', 'Orders', ['Order_id'], ['id'])
    op.create_foreign_key('Invoices_Plant_id_fkey', 'Invoices', 'Plant', ['Plant_id'], ['id'])
    op.create_foreign_key('Invoices_SoldTo_id_fkey', 'Invoices', 'Customers', ['SoldTo_id'], ['id'])
    op.create_foreign_key('Invoices_ShipTo_id_fkey', 'Invoices', 'Shipto', ['ShipTo_id'], ['id'])
    op.create_foreign_key('Invoices_Delivery_id_fkey', 'Invoices', 'Deliveries', ['Delivery_id'], ['id'])
    op.create_index('ix_Invoices_Order_id', 'Invoices', ['Order_id'], unique=False)
    op.create_table('InvoiceLines',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"InvoiceLines_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Invoice_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Pricing_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('GI_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('Act_GI_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('Material_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Ord_Status_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Qty', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('LineItem', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['Invoice_id'], ['Invoices.id'], name='InvoiceLines_Invoice_id_fkey'),
    sa.ForeignKeyConstraint(['Material_id'], ['Materials.id'], name='InvoiceLines_Material_id_fkey'),
    sa.ForeignKeyConstraint(['Ord_Status_id'], ['OrderStatus.id'], name='InvoiceLines_Ord_Status_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='InvoiceLines_pkey')
    )
    op.create_index('ix_InvoiceLines_Invoice_id', 'InvoiceLines', ['Invoice_id'], unique=False)
    # ### end Alembic commands ###