"""Invoice table corrected

Revision ID: b1c87168d205
Revises: 20c436feb618
Create Date: 2022-07-17 17:40:25.880738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c87168d205'
down_revision = '20c436feb618'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('InvoiceLines', sa.Column('LineItem', sa.Integer(), nullable=True))
    op.alter_column('InvoiceLines', 'GI_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('open_order_lines', 'GI_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('open_order_lines', 'GI_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('InvoiceLines', 'GI_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.drop_column('InvoiceLines', 'LineItem')
    # ### end Alembic commands ###