"""add user profile photo

Revision ID: a4e8b6c9d120
Revises: 648c42d991c9
Create Date: 2026-08-24 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "a4e8b6c9d120"
down_revision = "648c42d991c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("profile_photo", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "profile_photo")
