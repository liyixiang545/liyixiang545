"""empty message

Revision ID: 49e61c9c679b
Revises: 98a686f3f717
Create Date: 2022-03-29 15:19:41.118055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e61c9c679b'
down_revision = '98a686f3f717'
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
