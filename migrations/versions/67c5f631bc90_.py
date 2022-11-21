"""empty message

Revision ID: 67c5f631bc90
Revises: faf3914f94ce
Create Date: 2022-03-22 18:22:59.375542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c5f631bc90'
down_revision = 'faf3914f94ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'comment', 'user', ['Comment_id'], ['id'])
    op.add_column('user', sa.Column('img', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'img')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    # ### end Alembic commands ###