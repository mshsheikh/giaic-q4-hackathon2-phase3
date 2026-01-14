# Phase 1.4 - Database Schema Specification: Technical Documentation

**Date**: 2026-01-12
**Phase**: Hackathon 2 – Phase 3
**Step**: PHASE 1.4 – Database Schema Specification (SQLModel + Neon)

## Overview

This document provides a human-readable technical explanation of the Database Schema specification created in Phase 1.4. The goal was to define a canonical data model for the Todo AI Chatbot that supports stateless backend operations, ensures multi-user isolation, and provides the foundation for tasks, conversations, and messages.

## Purpose

The database schema serves as the persistent storage layer for the Todo AI Chatbot, storing user tasks, conversation histories, and message exchanges between users and the TodoAgent. It ensures data integrity, security, and performance for the stateless backend architecture.

## Key Technical Decisions

### 1. SQLModel ORM Selection
- Chosen for its compatibility with both SQLAlchemy and Pydantic
- Provides type safety and validation at the model level
- Enables easy serialization and deserialization of data
- Supports both sync and async operations

### 2. Neon Serverless PostgreSQL Target
- Selected for its serverless architecture that scales automatically
- Provides connection pooling and branching capabilities
- Offers improved developer experience with Git-like database branching
- Supports standard PostgreSQL features while optimizing for cloud environments

### 3. Stateless Backend Support
- All state is persisted in the database rather than in memory
- No session-based data storage is required
- Server restarts don't affect data availability
- Horizontal scaling is supported through database sharing

### 4. Multi-User Isolation
- All tables include user_id for ownership tracking
- Queries must filter by user_id to prevent cross-user access
- Indexes on user_id fields enable efficient filtering
- Application-level validation ensures user_id matches authenticated user

## Data Model Details

### Task Model
The Task model stores user todo items with the following characteristics:
- **Primary Key**: UUID-based id for global uniqueness
- **Ownership**: user_id field ensures multi-user isolation
- **Content**: title (required), description (optional), completed status (boolean)
- **Metadata**: created_at and updated_at timestamps
- **Indexes**: Optimized for user-based queries and completion status filtering

### Conversation Model
The Conversation model stores chat sessions with the following characteristics:
- **Primary Key**: UUID-based id for global uniqueness
- **Ownership**: user_id field ensures multi-user isolation
- **Metadata**: created_at and updated_at timestamps
- **Indexes**: Optimized for user-based queries and chronological ordering

### Message Model
The Message model stores individual messages within conversations with the following characteristics:
- **Primary Key**: UUID-based id for global uniqueness
- **Ownership**: user_id field ensures multi-user isolation
- **Relationship**: Foreign key to Conversation model
- **Content**: role (user|assistant|tool), content (text)
- **Metadata**: created_at timestamp
- **Indexes**: Optimized for conversation-based queries and chronological ordering

## Entity Relationships

The schema implements the following relationships:
- **One-to-Many**: User to Conversation (one user has many conversations)
- **One-to-Many**: User to Task (one user has many tasks)
- **One-to-Many**: Conversation to Message (one conversation contains many messages)

## Query Patterns

### Chat API Requirements
- **Conversation History**: Retrieve all messages for a conversation ordered chronologically
- **New Conversation Creation**: Insert new conversation records
- **Message Addition**: Insert new message records with proper associations

### MCP Tools Requirements
- **Task Management**: Retrieve, create, update, and delete user tasks
- **User Isolation**: Ensure all operations are scoped to the authenticated user

### Agent Replay Requirements
- **Full History**: Retrieve complete conversation history for context restoration
- **Metadata Queries**: Get conversation statistics and summaries

## Migration Strategy

### Initial Setup
- Tables created in dependency order (Task, Conversation, Message)
- Indexes applied after data population for performance
- Foreign key constraints validated after initial load

### Future Changes
- Alembic-based migration management
- Backward-compatible changes prioritized
- Blue-green deployment for disruptive changes
- Feature flags for gradual rollouts

## Neon-Specific Considerations

### Connection Management
- Connection pooling configured for serverless architecture
- Idle timeout settings aligned with Neon's session management
- Retry logic implemented for connection failures

### Performance Optimization
- Queries optimized to minimize connection time
- Efficient indexing strategy for common access patterns
- Resource usage monitored to optimize costs

### Security Features
- SSL/TLS encryption enforced for all connections
- Built-in Neon security features enabled
- Application-level authentication and authorization implemented

## Multi-User Isolation

### Database-Level Controls
- All tables include user_id for ownership tracking
- All queries must filter by user_id to prevent cross-user access
- Indexes on user_id fields for efficient filtering

### Application-Level Validation
- User_id validated against authenticated user
- Role-based access controls implemented
- Audit logging for security monitoring

## Constraints and Invariants

### Data Integrity
- Required field constraints enforced
- Value range constraints validated
- Foreign key relationships maintained
- Timestamp consistency ensured

### Business Logic
- User ownership maintained across all operations
- Conversation continuity preserved
- Task isolation enforced
- Message ordering maintained

## Implementation Requirements

### For Database Layer
- Must use SQLModel ORM for all operations
- Must target Neon Serverless PostgreSQL
- Must enforce all defined constraints
- Must maintain all specified indexes

### For Application Layer
- Must filter all queries by user_id
- Must validate user authentication
- Must handle connection pooling appropriately
- Must implement retry logic for transient failures

## Expected Outcomes

This specification enables the development of a robust, scalable database layer that can:
- Store and retrieve user tasks securely and efficiently
- Maintain conversation history across server restarts
- Support multi-user isolation with 100% accuracy
- Scale efficiently with Neon's serverless architecture
- Support the stateless backend architecture of the application

## Next Steps

1. Implement the database schema using SQLModel
2. Set up Neon Serverless PostgreSQL instance
3. Create initial Alembic migration
4. Deploy schema to development environment
5. Test query performance and adjust indexes as needed