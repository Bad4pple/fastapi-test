"""create posts table

Revision ID: 4c5e8fb8d560
Revises: 
Create Date: 2023-06-23 11:23:01.147366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c5e8fb8d560'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
