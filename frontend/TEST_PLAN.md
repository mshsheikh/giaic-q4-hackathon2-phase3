# End-to-End Workflow Verification

## Expected Flow

1. **User sends message**: User types a message in the chat UI and clicks "Send"
2. **Frontend request**: The chat component sends a POST request to `${process.env.NEXT_PUBLIC_BACKEND_API_URL}/${userId}/chat`
3. **Backend processing**: The backend receives the request at `/api/{user_id}/chat` endpoint
4. **Authentication**: The backend validates that the authenticated user matches the user_id in the path
5. **Context enrichment**: Request context is validated and enriched with user identity
6. **Message storage**: User's message is saved to the database
7. **Agent processing**: TodoAgent processes the request, potentially triggering MCP tools
8. **Tool execution**: If MCP tools are needed (add_task, list_tasks, complete_task, etc.), they are executed
9. **Response storage**: Agent's response is saved to the database
10. **Tool logging**: Any tool calls made are logged
11. **Response formatting**: Response is formatted with conversation_id, response text, and tool_calls
12. **Frontend receives**: Frontend receives the response and displays it
13. **Tool rendering**: Tool calls are rendered in the chat UI if present
14. **Multi-user isolation**: Each user's conversations and tasks are isolated by user_id

## MCP Tools Integration

The following MCP tools should be available and functional:
- `add_task`: Creates a new task in the database
- `list_tasks`: Retrieves tasks for the current user
- `complete_task`: Marks a task as completed
- `delete_task`: Removes a task from the database
- `update_task`: Modifies an existing task

## Testing Scenarios

1. **Basic chat**: "Hello" → Should receive a greeting response
2. **Task creation**: "Add 'buy groceries' to my tasks" → Should trigger add_task tool
3. **Task listing**: "Show my tasks" → Should trigger list_tasks tool
4. **Task completion**: "Complete task 1" → Should trigger complete_task tool
5. **Task deletion**: "Delete 'buy groceries'" → Should trigger delete_task tool
6. **Task update**: "Update 'buy groceries' to 'buy milk instead'" → Should trigger update_task tool