# Chat API Specification: Todo AI Chatbot

## Overview
This document defines the Chat API for the Todo AI Chatbot. The API serves as the interface between clients and the TodoAgent, handling natural language requests and orchestrating MCP tool calls through the OpenAI Agent.

## Endpoint Definition

### POST /api/{user_id}/chat

#### Purpose
Processes a natural language message from a user and returns the TodoAgent's response along with any tool calls that were made.

#### Path Parameters
- `user_id` (string, required): Unique identifier of the user making the request

#### Request Schema
```json
{
  "message": {
    "type": "string",
    "description": "Natural language message from the user",
    "maxLength": 1000,
    "required": true
  },
  "conversation_id": {
    "type": "string",
    "description": "Unique identifier of the conversation (optional)",
    "format": "UUID",
    "required": false
  }
}
```

#### Example Request
```json
{
  "message": "Add 'buy groceries' to my todo list",
  "conversation_id": "abc123-def456-ghi789"
}
```

#### Response Schema
```json
{
  "success": {
    "type": "boolean",
    "description": "Indicates if the request was successful"
  },
  "conversation_id": {
    "type": "string",
    "description": "Unique identifier of the conversation (new or existing)"
  },
  "response": {
    "type": "string",
    "description": "The assistant's response to the user's message"
  },
  "tool_calls": {
    "type": "array",
    "description": "List of MCP tool calls made by the agent",
    "items": {
      "type": "object",
      "properties": {
        "tool_name": {
          "type": "string",
          "description": "Name of the MCP tool called"
        },
        "parameters": {
          "type": "object",
          "description": "Parameters passed to the tool"
        },
        "result": {
          "type": "object",
          "description": "Result returned by the tool"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the tool was called"
        }
      }
    }
  },
  "error": {
    "type": "object",
    "description": "Error information if the request failed",
    "properties": {
      "code": {
        "type": "string",
        "description": "Error code"
      },
      "message": {
        "type": "string",
        "description": "Human-readable error message"
      }
    },
    "required": ["code", "message"],
    "nullable": true
  }
}
```

#### Example Response
```json
{
  "success": true,
  "conversation_id": "abc123-def456-ghi789",
  "response": "I've added 'buy groceries' to your todo list.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "user_id": "user123",
        "description": "buy groceries",
        "priority": "medium"
      },
      "result": {
        "success": true,
        "task": {
          "id": "task789",
          "user_id": "user123",
          "description": "buy groceries",
          "status": "pending",
          "priority": "medium",
          "created_at": "2026-01-12T15:00:00.000Z",
          "updated_at": "2026-01-12T15:00:00.000Z"
        }
      },
      "timestamp": "2026-01-12T15:00:00.000Z"
    }
  ],
  "error": null
}
```

## Request Lifecycle

The following steps outline the complete lifecycle of a request to the Chat API:

### Step 1: Request Validation
- Validate the incoming request payload
- Verify that `user_id` is in a valid format
- Verify that `message` is present and not empty
- If `conversation_id` is provided, verify it's in a valid UUID format

### Step 2: Conversation Initialization
- If `conversation_id` is not provided:
  - Generate a new unique conversation ID (UUID)
  - Create a new conversation record in the database with the user_id
- If `conversation_id` is provided:
  - Verify the conversation exists in the database
  - Verify the user_id matches the conversation owner
  - If verification fails, return an appropriate error

### Step 3: Message Persistence
- Create a new message record in the database:
  - Type: "user"
  - Content: the provided message
  - Associated with the conversation_id
  - Timestamp: current time

### Step 4: Conversation History Retrieval
- Query the database to retrieve all messages for the conversation
- Order messages chronologically
- Ensure only messages belonging to the correct user and conversation are retrieved

### Step 5: OpenAI Agent Invocation
- Prepare the message history in the format required by the OpenAI Agent
- Invoke the TodoAgent with the full conversation history
- The agent processes the message and may call MCP tools as needed

### Step 6: MCP Tool Execution
- The TodoAgent calls MCP tools as needed based on the user's request
- Tool calls are executed through the MCP interface
- Tool results are captured and returned to the agent
- All tool calls and their results are logged for audit purposes

### Step 7: Assistant Response Generation
- The agent generates a natural language response based on:
  - The user's original message
  - Results from any MCP tool calls
  - Previous conversation history
- The response is returned to the API

### Step 8: Response Persistence
- Create a new message record in the database:
  - Type: "assistant"
  - Content: the assistant's response
  - Associated with the conversation_id
  - Timestamp: current time

### Step 9: Tool Call Logging
- For each MCP tool called during the request:
  - Log the tool call with parameters and results
  - Associate the log entry with the conversation_id
  - Include timestamp information

### Step 10: API Response Construction
- Construct the response object containing:
  - conversation_id
  - assistant response text
  - List of tool calls made (if any)
  - Success status
  - Error information (if applicable)

## Stateless Execution Guarantees

### Memory Management
- The API maintains no in-memory state between requests
- All conversation state is retrieved from the database at the beginning of each request
- No session objects or cached data are maintained between requests
- Each request is processed independently

### Data Persistence
- All conversation data is stored in the database
- Message history is retrieved from the database for each request
- All new messages are immediately persisted to the database
- Tool call logs are stored in the database for audit purposes

### Server Restart Resilience
- Server restarts do not affect ongoing conversations
- All conversation state is preserved in the database
- Clients can resume conversations after server restarts
- No in-memory caches need to be warmed up after restarts

## Multi-User Isolation Rules

### User Identification
- All requests must include a valid user_id
- The user_id is validated against the authenticated user
- Requests cannot access conversations belonging to other users

### Conversation Access Control
- Conversations are associated with a specific user_id
- Users can only access conversations they own
- Conversation retrieval queries always filter by user_id
- Unauthorized access attempts result in appropriate errors

### Data Segregation
- Database queries always include user_id in WHERE clauses
- No cross-user data access is possible
- Tool calls are scoped to the requesting user
- Conversation history is filtered by user ownership

## Error Handling Rules

### Client-Side Errors (4xx)
- Invalid request format: Return 400 Bad Request
- Unauthorized access: Return 401 Unauthorized
- Forbidden access: Return 403 Forbidden
- Missing conversation: Return 404 Not Found

### Server-Side Errors (5xx)
- Database connectivity issues: Return 500 Internal Server Error
- MCP tool unavailability: Return 500 Internal Server Error
- OpenAI Agent unavailability: Return 500 Internal Server Error
- Unexpected server errors: Return 500 Internal Server Error

### Error Response Format
All errors follow the same format as the success response, with:
- `success`: false
- `error` object populated with code and message
- Other fields set to null or empty values as appropriate

## Restart/Resume Behavior

### Conversation Continuity
- Conversations persist across server restarts
- All conversation history remains available in the database
- Clients can continue conversations after server restarts
- No loss of conversation state occurs during restarts

### Session Recovery
- No session recovery mechanism needed (stateless design)
- Clients simply make requests with the conversation_id
- API retrieves full conversation history from database
- Normal processing continues as if no interruption occurred

### Data Integrity
- Database transactions ensure data consistency
- Failed requests don't corrupt existing conversations
- Message ordering is preserved through timestamps
- Tool call logs maintain integrity across restarts

## Implementation Requirements

### FastAPI Framework
- Use FastAPI for routing and request handling
- Leverage FastAPI's automatic validation and documentation features
- Implement proper type hints for all endpoints
- Use dependency injection for services and database connections

### OpenAI Agent Integration
- Integrate with OpenAI Agents SDK for agent processing
- Pass full conversation history to the agent
- Handle agent responses and tool calls appropriately
- Implement proper error handling for agent operations

### MCP Tool Integration
- All tool calls must go through the MCP interface
- Direct tool calls from the API are prohibited
- Capture and log all tool interactions
- Ensure proper authentication for all tool calls