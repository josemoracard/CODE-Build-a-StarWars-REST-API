"""empty message

Revision ID: 76fe03922a6c
Revises: 290ff3f70f67
Create Date: 2023-03-09 19:48:59.112027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76fe03922a6c'
down_revision = '290ff3f70f67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='favorites_character_id_fkey'),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], name='favorites_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorites_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey')
    )
    op.drop_table('favorite_planets')
    op.drop_table('favorite_characters')
    # ### end Alembic commands ###
