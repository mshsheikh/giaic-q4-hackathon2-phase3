"""
Add name and description fields to conversations table

Revision ID: 002
Revises: 001
Create Date: 2026-01-12 21:30:00.000000

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add name column to conversations table
    op.add_column('conversations', sa.Column('name', sa.String(length=255), nullable=True))

    # Add description column to conversations table
    op.add_column('conversations', sa.Column('description', sa.String(length=1000), nullable=True))


def downgrade() -> None:
    # Remove description column from conversations table
    op.drop_column('conversations', 'description')

    # Remove name column from conversations table
    op.drop_column('conversations', 'name')