"""creating posts users foreign_key owner_id

Revision ID: fcb7b8058f4b
Revises: b7963308d39a
Create Date: 2026-04-18 19:15:42.022360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcb7b8058f4b'
down_revision: Union[str, Sequence[str], None] = 'b7963308d39a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer))
    op.create_foreign_key('posts_users_fk','posts','users',['owner_id'], ['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
