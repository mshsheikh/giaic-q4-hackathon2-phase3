# MCP Tool Specification: Todo AI Chatbot

## Overview
This document defines the MCP (Model Context Protocol) tools for the Todo AI Chatbot. These stateless tools enable the TodoAgent to perform all task management operations through standardized interfaces.

## Global MCP Rules
- Tools must never assume prior calls
- Tools must never depend on agent memory
- All user scoping must be enforced via user_id
- Tools must return structured, predictable responses
- Errors must be machine-readable and human-safe
- All tools must be fully stateless with no in-memory storage
- All state must be persisted to the database
- Strict input/output schemas must be enforced

## Tool Specifications

### 1. add_task

#### Purpose
Creates a new task for the specified user in the database.

#### Input Parameters
- `user_id` (string, required): Unique identifier of the user
- `description` (string, required): Description of the task
- `priority` (string, optional): Priority level (low, medium, high) - defaults to "medium"
- `due_date` (string, optional): Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)

#### Output Schema
```json
{
  "success": boolean,
  "task": {
    "id": string,
    "user_id": string,
    "description": string,
    "status": "pending",
    "priority": string,
    "created_at": string,
    "updated_at": string,
    "due_date": string (nullable)
  },
  "error": {
    "code": string,
    "message": string
  }
}
```

#### Example Input
```json
{
  "user_id": "user123",
  "description": "Buy groceries",
  "priority": "high",
  "due_date": "2026-01-15T00:00:00.000Z"
}
```

#### Example Output
```json
{
  "success": true,
  "task": {
    "id": "task456",
    "user_id": "user123",
    "description": "Buy groceries",
    "status": "pending",
    "priority": "high",
    "created_at": "2026-01-12T14:30:00.000Z",
    "updated_at": "2026-01-12T14:30:00.000Z",
    "due_date": "2026-01-15T00:00:00.000Z"
  },
  "error": null
}
```

#### Error Cases
- Invalid input parameters (missing required fields, invalid data types)
- User not found or unauthorized access
- Database connection errors
- Duplicate constraint violations (if applicable)

#### Stateless Execution Rules
- Does not rely on any previous state or session data
- Creates a new task record in the database with all required information
- Generates a unique task ID upon successful creation

#### Database Interaction Responsibility
- Inserts a new task record into the tasks table
- Validates user_id exists and is authorized
- Sets initial status to "pending"
- Sets created_at and updated_at timestamps

#### Idempotency Considerations
- Not idempotent by design (each call creates a new task)
- Different task IDs will be generated for each call

---

### 2. list_tasks

#### Purpose
Retrieves all tasks for the specified user from the database.

#### Input Parameters
- `user_id` (string, required): Unique identifier of the user
- `status_filter` (string, optional): Filter by status (pending, completed) - defaults to all statuses
- `limit` (integer, optional): Maximum number of tasks to return - defaults to 100
- `offset` (integer, optional): Number of tasks to skip for pagination - defaults to 0

#### Output Schema
```json
{
  "success": boolean,
  "tasks": [
    {
      "id": string,
      "user_id": string,
      "description": string,
      "status": string,
      "priority": string,
      "created_at": string,
      "updated_at": string,
      "due_date": string (nullable)
    }
  ],
  "pagination": {
    "total": integer,
    "limit": integer,
    "offset": integer
  },
  "error": {
    "code": string,
    "message": string
  }
}
```

#### Example Input
```json
{
  "user_id": "user123",
  "status_filter": "pending",
  "limit": 10,
  "offset": 0
}
```

#### Example Output
```json
{
  "success": true,
  "tasks": [
    {
      "id": "task456",
      "user_id": "user123",
      "description": "Buy groceries",
      "status": "pending",
      "priority": "high",
      "created_at": "2026-01-12T14:30:00.000Z",
      "updated_at": "2026-01-12T14:30:00.000Z",
      "due_date": "2026-01-15T00:00:00.000Z"
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 10,
    "offset": 0
  },
  "error": null
}
```

#### Error Cases
- Invalid user_id format
- User not found or unauthorized access
- Database connection errors
- Invalid filter parameters

#### Stateless Execution Rules
- Does not rely on any previous state or session data
- Queries the database directly for tasks matching the user_id
- Applies filters and limits as specified in input

#### Database Interaction Responsibility
- Selects tasks from the tasks table where user_id matches
- Applies status filtering if specified
- Implements pagination using LIMIT and OFFSET

#### Idempotency Considerations
- Fully idempotent - same inputs will produce the same results (assuming no concurrent changes)

---

### 3. complete_task

#### Purpose
Marks a specific task as completed in the database.

#### Input Parameters
- `user_id` (string, required): Unique identifier of the user
- `task_id` (string, required): Unique identifier of the task to complete

#### Output Schema
```json
{
  "success": boolean,
  "task": {
    "id": string,
    "user_id": string,
    "description": string,
    "status": "completed",
    "priority": string,
    "created_at": string,
    "updated_at": string,
    "due_date": string (nullable)
  },
  "error": {
    "code": string,
    "message": string
  }
}
```

#### Example Input
```json
{
  "user_id": "user123",
  "task_id": "task456"
}
```

#### Example Output
```json
{
  "success": true,
  "task": {
    "id": "task456",
    "user_id": "user123",
    "description": "Buy groceries",
    "status": "completed",
    "priority": "high",
    "created_at": "2026-01-12T14:30:00.000Z",
    "updated_at": "2026-01-12T15:00:00.000Z",
    "due_date": "2026-01-15T00:00:00.000Z"
  },
  "error": null
}
```

#### Error Cases
- Task not found
- Task belongs to a different user (authorization error)
- Invalid input parameters
- Database connection errors

#### Stateless Execution Rules
- Does not rely on any previous state or session data
- Updates the specific task record in the database
- Verifies user owns the task before updating

#### Database Interaction Responsibility
- Updates the status field to "completed" in the tasks table
- Updates the updated_at timestamp
- Verifies user_id matches the task owner

#### Idempotency Considerations
- Idempotent - calling multiple times with same parameters will result in task being completed

---

### 4. delete_task

#### Purpose
Removes a specific task from the database.

#### Input Parameters
- `user_id` (string, required): Unique identifier of the user
- `task_id` (string, required): Unique identifier of the task to delete

#### Output Schema
```json
{
  "success": boolean,
  "deleted_task_id": string,
  "error": {
    "code": string,
    "message": string
  }
}
```

#### Example Input
```json
{
  "user_id": "user123",
  "task_id": "task456"
}
```

#### Example Output
```json
{
  "success": true,
  "deleted_task_id": "task456",
  "error": null
}
```

#### Error Cases
- Task not found
- Task belongs to a different user (authorization error)
- Invalid input parameters
- Database connection errors

#### Stateless Execution Rules
- Does not rely on any previous state or session data
- Deletes the specific task record from the database
- Verifies user owns the task before deletion

#### Database Interaction Responsibility
- Deletes the record from the tasks table where task_id and user_id match
- Returns confirmation of the deleted task ID

#### Idempotency Considerations
- Not idempotent after first call (subsequent calls will result in "task not found" error)

---

### 5. update_task

#### Purpose
Modifies the properties of a specific task in the database.

#### Input Parameters
- `user_id` (string, required): Unique identifier of the user
- `task_id` (string, required): Unique identifier of the task to update
- `description` (string, optional): New description for the task
- `status` (string, optional): New status (pending, completed)
- `priority` (string, optional): New priority level (low, medium, high)
- `due_date` (string, optional): New due date in ISO 8601 format

#### Output Schema
```json
{
  "success": boolean,
  "task": {
    "id": string,
    "user_id": string,
    "description": string,
    "status": string,
    "priority": string,
    "created_at": string,
    "updated_at": string,
    "due_date": string (nullable)
  },
  "error": {
    "code": string,
    "message": string
  }
}
```

#### Example Input
```json
{
  "user_id": "user123",
  "task_id": "task456",
  "description": "Buy groceries and household items",
  "priority": "medium"
}
```

#### Example Output
```json
{
  "success": true,
  "task": {
    "id": "task456",
    "user_id": "user123",
    "description": "Buy groceries and household items",
    "status": "pending",
    "priority": "medium",
    "created_at": "2026-01-12T14:30:00.000Z",
    "updated_at": "2026-01-12T15:30:00.000Z",
    "due_date": "2026-01-15T00:00:00.000Z"
  },
  "error": null
}
```

#### Error Cases
- Task not found
- Task belongs to a different user (authorization error)
- Invalid input parameters
- Database connection errors
- Invalid status value

#### Stateless Execution Rules
- Does not rely on any previous state or session data
- Updates only the specified fields in the task record
- Verifies user owns the task before updating

#### Database Interaction Responsibility
- Updates specified fields in the tasks table
- Updates the updated_at timestamp
- Verifies user_id matches the task owner

#### Idempotency Considerations
- Idempotent when same parameters are provided multiple times (updating with same values)

## Implementation Requirements

### MCP SDK Compliance
- All tools must be implemented using the Official MCP SDK
- Proper error handling and logging must be implemented
- Input validation must occur before any database operations

### Statelessness
- No in-memory state storage allowed
- Each tool call must be independent
- All state must be retrieved from and stored to the database

### Security
- User authentication and authorization must be verified for each operation
- User isolation must be enforced (users can only access their own tasks)
- Input sanitization must prevent injection attacks