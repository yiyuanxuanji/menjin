"""dierci4

Revision ID: 598754c09616
Revises: 17ece265e858
Create Date: 2018-05-23 23:09:35.684434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '598754c09616'
down_revision = '17ece265e858'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fk_yanzheng',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('info_data', sa.String(length=100), nullable=False),
    sa.Column('info', sa.String(length=1000), nullable=False),
    sa.Column('open_id', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fk_yanzheng')
    # ### end Alembic commands ###