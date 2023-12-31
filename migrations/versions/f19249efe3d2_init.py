"""init

Revision ID: f19249efe3d2
Revises:
Create Date: 2022-05-17 21:13:06.181138

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'f19249efe3d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('citymodel',
        sa.Column('id_city', sa.Integer(), nullable=True),
        sa.Column('name_city', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('postal_code', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id_city')
    )
    op.create_table('usermodel',
        sa.Column('id_user', sa.Integer(), nullable=True),
        sa.Column('name_user', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id_user')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usermodel')
    op.drop_table('citymodel')
    # ### end Alembic commands ###
