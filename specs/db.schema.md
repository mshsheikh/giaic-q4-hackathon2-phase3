# Database Schema Specification: Todo AI Chatbot

## Overview
This document defines the database schema for the Todo AI Chatbot, implemented using SQLModel ORM and targeting Neon Serverless PostgreSQL. The schema supports stateless backend operations, ensures multi-user isolation, and provides the data foundation for tasks, conversations, and messages.

## Database Configuration

### Target Platform
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Connection Pooling**: Connection pooling should be configured with appropriate settings for Neon's serverless architecture
- **Migration Tool**: Alembic for schema evolution

## Data Models

### 1. Task Model

#### Purpose
Stores user todo items with completion status and metadata.

#### Field Definitions
- `id` (UUID, Primary Key, Required)
  - Type: UUID (PostgreSQL native UUID type)
  - Default: Generated automatically
  - Constraints: Primary key, not null
- `user_id` (String, Required)
  - Type: VARCHAR(255)
  - Constraints: Not null, indexed for multi-user isolation
- `title` (String, Required)
  - Type: VARCHAR(255)
  - Constraints: Not null
- `description` (String, Optional)
  - Type: TEXT
  - Constraints: Nullable
- `completed` (Boolean, Required)
  - Type: BOOLEAN
  - Default: false
  - Constraints: Not null
- `created_at` (DateTime, Required)
  - Type: TIMESTAMP WITH TIME ZONE
  - Default: Current timestamp
  - Constraints: Not null
- `updated_at` (DateTime, Required)
  - Type: TIMESTAMP WITH TIME ZONE
  - Default: Current timestamp
  - Constraints: Not null, auto-updated on changes

#### SQLModel Implementation
```python
from sqlmodel import SQLModel, Field, create_engine, Session
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

#### Indexes
- `idx_task_user_id`: Index on user_id for efficient user-based queries
- `idx_task_completed`: Index on completed status for filtering
- `idx_task_user_completed`: Composite index on (user_id, completed) for common queries

#### Constraints
- NOT NULL constraints on required fields
- Primary key constraint on id
- Check constraint to ensure title is not empty

#### Multi-User Isolation
- All queries must filter by user_id to ensure users only access their own tasks
- Index on user_id enables efficient filtering

---

### 2. Conversation Model

#### Purpose
Stores conversation sessions between users and the TodoAgent.

#### Field Definitions
- `id` (UUID, Primary Key, Required)
  - Type: UUID (PostgreSQL native UUID type)
  - Default: Generated automatically
  - Constraints: Primary key, not null
- `user_id` (String, Required)
  - Type: VARCHAR(255)
  - Constraints: Not null, indexed for multi-user isolation
- `created_at` (DateTime, Required)
  - Type: TIMESTAMP WITH TIME ZONE
  - Default: Current timestamp
  - Constraints: Not null
- `updated_at` (DateTime, Required)
  - Type: TIMESTAMP WITH TIME ZONE
  - Default: Current timestamp
  - Constraints: Not null, auto-updated on changes

#### SQLModel Implementation
```python
class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

#### Indexes
- `idx_conversation_user_id`: Index on user_id for efficient user-based queries
- `idx_conversation_created_at`: Index on created_at for chronological ordering

#### Constraints
- NOT NULL constraints on required fields
- Primary key constraint on id

#### Multi-User Isolation
- All queries must filter by user_id to ensure users only access their own conversations
- Index on user_id enables efficient filtering

---

### 3. Message Model

#### Purpose
Stores individual messages within conversations, including user messages, assistant responses, and tool calls.

#### Field Definitions
- `id` (UUID, Primary Key, Required)
  - Type: UUID (PostgreSQL native UUID type)
  - Default: Generated automatically
  - Constraints: Primary key, not null
- `user_id` (String, Required)
  - Type: VARCHAR(255)
  - Constraints: Not null, indexed for multi-user isolation
- `conversation_id` (UUID, Required, Foreign Key)
  - Type: UUID (References Conversation.id)
  - Constraints: Not null, foreign key constraint
- `role` (String, Required)
  - Type: VARCHAR(20)
  - Constraints: Not null, check constraint to allow only 'user', 'assistant', 'tool'
- `content` (String, Required)
  - Type: TEXT
  - Constraints: Not null
- `created_at` (DateTime, Required)
  - Type: TIMESTAMP WITH TIME ZONE
  - Default: Current timestamp
  - Constraints: Not null

#### SQLModel Implementation
```python
from sqlmodel import Relationship

class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    conversation_id: UUID = Field(foreign_key="conversation.id", nullable=False)
    role: str = Field(max_length=20, nullable=False)  # 'user', 'assistant', 'tool'
    content: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
```

#### Indexes
- `idx_message_user_id`: Index on user_id for efficient user-based queries
- `idx_message_conversation_id`: Index on conversation_id for conversation-based queries
- `idx_message_conversation_created`: Composite index on (conversation_id, created_at) for chronological message retrieval
- `idx_message_role`: Index on role for filtering by message type

#### Constraints
- NOT NULL constraints on required fields
- Primary key constraint on id
- Foreign key constraint linking to Conversation table
- Check constraint to ensure role is one of 'user', 'assistant', or 'tool'

#### Multi-User Isolation
- All queries must filter by user_id to ensure users only access their own messages
- Combined with conversation_id filtering for additional security

## Entity Relationship Diagram (ERD)

```
[User] 1----* [Conversation] 1----* [Message]
              |
              * [Task]
```

### Relationships
- **Conversation to Message**: One-to-Many (one conversation contains many messages)
- **User to Conversation**: One-to-Many (one user has many conversations)
- **User to Task**: One-to-Many (one user has many tasks)
- **Conversation to Task**: Indirect relationship through user_id

## Query Patterns

### Chat API Requirements
1. **Get conversation history**: Retrieve all messages for a specific conversation ordered by created_at
   - Query: `SELECT * FROM message WHERE conversation_id = ? AND user_id = ? ORDER BY created_at`
   - Index: `idx_message_conversation_created`

2. **Create new conversation**: Insert a new conversation record
   - Query: `INSERT INTO conversation (user_id) VALUES (?)`

3. **Add message to conversation**: Insert a new message record
   - Query: `INSERT INTO message (user_id, conversation_id, role, content) VALUES (?, ?, ?, ?)`

### MCP Tools Requirements
1. **Get user tasks**: Retrieve all tasks for a specific user
   - Query: `SELECT * FROM task WHERE user_id = ?`
   - Index: `idx_task_user_id`

2. **Create task**: Insert a new task record
   - Query: `INSERT INTO task (user_id, title, description) VALUES (?, ?, ?)`

3. **Update task**: Update an existing task record
   - Query: `UPDATE task SET completed = ?, updated_at = ? WHERE id = ? AND user_id = ?`
   - Index: Primary key on id with user_id check

### Agent Replay Requirements
1. **Full conversation history**: Retrieve complete message history for a conversation
   - Query: `SELECT * FROM message WHERE conversation_id = ? AND user_id = ? ORDER BY created_at ASC`
   - Index: `idx_message_conversation_created`

2. **Conversation metadata**: Get conversation details with message count
   - Query: `SELECT c.*, COUNT(m.id) as message_count FROM conversation c LEFT JOIN message m ON c.id = m.conversation_id WHERE c.user_id = ? GROUP BY c.id`

## Migration Strategy

### Initial Schema Migration
1. Create tables in dependency order:
   - First: Task table
   - Second: Conversation table
   - Third: Message table (depends on Conversation)

2. Create indexes after tables are populated for better performance

3. Set up foreign key constraints after initial data load if needed

### Future Schema Changes
1. Use Alembic for migration management
2. Follow backward-compatible changes when possible
3. Implement blue-green deployment for schema changes that require downtime
4. Use feature flags to enable new schema features gradually

### Migration Example
```python
# Example Alembic migration for adding a new field
def upgrade() -> None:
    op.add_column('task', sa.Column('priority', sa.String(20), server_default='medium'))
    op.create_index('idx_task_priority', 'task', ['priority'])

def downgrade() -> None:
    op.drop_index('idx_task_priority')
    op.drop_column('task', 'priority')
```

## Neon-Specific Considerations

### Connection Management
- Configure connection pooling with appropriate settings for Neon's serverless architecture
- Set idle connection timeout to align with Neon's session management
- Implement retry logic for connection failures due to serverless scaling

### Performance Considerations
- Optimize queries to minimize connection time due to serverless nature
- Use connection pooling to reduce connection establishment overhead
- Consider read replicas for read-heavy operations if needed

### Scaling Considerations
- Neon automatically scales compute resources based on demand
- Monitor connection limits and adjust application pooling accordingly
- Design queries to be efficient to minimize resource usage

### Security Considerations
- Enable Neon's built-in security features
- Use encrypted connections (SSL/TLS)
- Implement proper authentication and authorization at the application level

## Multi-User Isolation Enforcement

### Database-Level Isolation
1. All tables include user_id field for ownership tracking
2. All queries must filter by user_id to prevent cross-user access
3. Indexes on user_id fields for efficient filtering
4. Application-level validation to ensure user_id matches authenticated user

### Query Examples with Isolation
```sql
-- Safe query pattern with user isolation
SELECT * FROM task WHERE user_id = 'authenticated_user_id';

-- Unsafe query that could allow cross-user access
SELECT * FROM task WHERE title = 'some_title'; -- Missing user_id filter
```

## Constraints and Invariants

### Data Integrity Constraints
1. **Task Title Non-Empty**: Tasks must have non-empty titles
2. **Message Role Validation**: Message roles must be 'user', 'assistant', or 'tool'
3. **Timestamp Consistency**: updated_at should never be before created_at
4. **Foreign Key Integrity**: Message conversation_id must reference existing conversation

### Business Logic Constraints
1. **User Ownership**: All records are owned by a specific user
2. **Conversation Continuity**: Messages belong to valid conversations
3. **Task Isolation**: Tasks cannot be shared between users
4. **Message Ordering**: Messages within conversations maintain chronological order