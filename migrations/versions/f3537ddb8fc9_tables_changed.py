"""tables changed

Revision ID: f3537ddb8fc9
Revises: 12e7bd0ef249
Create Date: 2022-07-03 18:19:11.976028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3537ddb8fc9'
down_revision = '12e7bd0ef249'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Producer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Producer_Code', sa.String(), nullable=False),
    sa.Column('Producer_Name', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Producer_Code')
    )
    op.drop_constraint('Materials_Producer_id_fkey', 'Materials', type_='foreignkey')
    op.create_foreign_key(None, 'Materials', 'Producer', ['Producer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Materials', type_='foreignkey')
    op.create_foreign_key('Materials_Producer_id_fkey', 'Materials', 'Plant', ['Producer_id'], ['id'])
    op.drop_table('Producer')
    # ### end Alembic commands ###
