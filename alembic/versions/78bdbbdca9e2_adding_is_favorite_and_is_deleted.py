"""Adding is_favorite and is_deleted

Revision ID: 78bdbbdca9e2
Revises: e79393806047
Create Date: 2026-07-26 15:20:23.163461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78bdbbdca9e2'
down_revision: Union[str, Sequence[str], None] = 'e79393806047'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
