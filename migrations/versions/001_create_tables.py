"""create_tables

Revision ID: 001
Revises: 
Create Date: 2025-09-03 15:05:13.702960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # USERS
    op.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username VARCHAR(100),
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    # TASKS
    op.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(user_id),
            task_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            is_completed BOOLEAN DEFAULT FALSE
        )
    ''')
    # ADD indices
    op.execute('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)')
    op.execute('CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at)')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP TABLE IF EXISTS tasks')
    op.execute('DROP TABLE IF EXISTS users')
