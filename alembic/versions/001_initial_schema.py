"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-12 16:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on user_id for tasks
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])

    # Create index on status for tasks
    op.create_index('ix_tasks_status', 'tasks', ['status'])

    # Create index on user_id and status for tasks
    op.create_index('ix_tasks_user_id_status', 'tasks', ['user_id', 'status'])


    # Create the conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on user_id for conversations
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])

    # Create index on created_at for conversations
    op.create_index('ix_conversations_created_at', 'conversations', ['created_at'])


    # Create the messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on user_id for messages
    op.create_index('ix_messages_user_id', 'messages', ['user_id'])

    # Create index on conversation_id for messages
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])

    # Create index on conversation_id and created_at for messages
    op.create_index('ix_messages_conversation_created', 'messages', ['conversation_id', 'created_at'])

    # Create index on role for messages
    op.create_index('ix_messages_role', 'messages', ['role'])


def downgrade() -> None:
    # Drop the messages table
    op.drop_index('ix_messages_role')
    op.drop_index('ix_messages_conversation_created')
    op.drop_index('ix_messages_conversation_id')
    op.drop_index('ix_messages_user_id')
    op.drop_table('messages')

    # Drop the conversations table
    op.drop_index('ix_conversations_created_at')
    op.drop_index('ix_conversations_user_id')
    op.drop_table('conversations')

    # Drop the tasks table
    op.drop_index('ix_tasks_user_id_status')
    op.drop_index('ix_tasks_status')
    op.drop_index('ix_tasks_user_id')
    op.drop_table('tasks')