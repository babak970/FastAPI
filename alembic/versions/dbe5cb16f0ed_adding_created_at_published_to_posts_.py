"""adding created_at & published to posts table

Revision ID: dbe5cb16f0ed
Revises: fcb7b8058f4b
Create Date: 2026-04-18 19:21:49.369189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbe5cb16f0ed'
down_revision: Union[str, Sequence[str], None] = 'fcb7b8058f4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()))
    op.add_column('posts',sa.Column('published',sa.BOOLEAN, nullable=False, server_default=sa.text("True")))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
