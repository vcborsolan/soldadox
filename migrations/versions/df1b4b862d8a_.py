"""empty message

Revision ID: df1b4b862d8a
Revises: 
Create Date: 2020-01-09 15:09:44.210965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df1b4b862d8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('initials', sa.String(length=2), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ddd',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('ddd_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ddd_id'], ['ddd.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('region')
    op.drop_table('ddd')
    op.drop_table('state')
    # ### end Alembic commands ###