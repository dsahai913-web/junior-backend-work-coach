"""add idempotency key to tasks

Revision ID: 74e1736263ee
Revises: 28bd7331a973
Create Date: 2026-10-01 13:13:16.022653

"""
from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74e1736263ee'
down_revision: Union[str, Sequence[str], None] = '28bd7331a973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('task',sa.Column('idempotency_key',sa.String(),nullable=True,unique=True))
    op.create_index(op.f('ix_task_idempotency_key'),'task',['idempotency_key'],unique=True)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_task_idempotency_key'),table_name='task')
    op.drop_column('task','idempotency_key')
