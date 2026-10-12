"""add ai explanation to tasks

Revision ID: 28bd7331a973
Revises: 1a3d899456a3
Create Date: 2026-10-01 11:49:14.865944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28bd7331a973'
down_revision: Union[str, Sequence[str], None] = '1a3d899456a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('task',
                  sa.Column('ai_explanation',sa.Text(),nullable=True),)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('task','ai_explanation')
