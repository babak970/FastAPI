"""creating_posts_table

Revision ID: f954057f70a4
Revises: 
Create Date: 2026-04-14 18:42:15.557026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f954057f70a4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('title',sa.String(),nullable=False ))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
