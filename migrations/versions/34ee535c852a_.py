"""empty message

Revision ID: 34ee535c852a
Revises: 1ea553645967
Create Date: 2022-04-16 22:16:00.219049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34ee535c852a'
down_revision = '1ea553645967'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'comment', 'user', ['Comment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    # ### end Alembic commands ###
