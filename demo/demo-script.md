# Todo AI Chatbot Demo Script

## Overview
This script provides a step-by-step demonstration of the Todo AI Chatbot system, highlighting its key features and capabilities. The demo showcases the system's ability to understand natural language requests and manage todo lists through AI-powered interactions.

## Runtime Verification Status
✅ **VERIFIED** - All Phase 4 runtime verification requirements have been successfully completed:
- Backend FastAPI startup and endpoint verification
- MCP server tool registration and communication
- Agent → MCP → DB flow validation
- Stateless conversation replay functionality
- Comprehensive error handling behavior
- Security, performance, and observability verification
- Demo readiness and frontend integration

## Prerequisites
- System is deployed and accessible
- Database is initialized and connected
- MCP server is running
- Agent is properly configured with OpenAI API key
- Frontend is accessible via web interface
- All components have passed runtime verification (check verification/runtime-checklist.md)
- Environment properly configured with .env files
- All security and observability features enabled

## Demo Setup
1. Navigate to the Todo AI Chatbot web interface
2. Ensure you're logged in (or demonstrate the login process if needed)
3. Verify the system is responsive and ready for interaction
4. Have sample user scenarios prepared for demonstration

## Demo Flow

### Opening (2 minutes)
1. **Introduction**
   - Welcome audience to the Todo AI Chatbot demonstration
   - Brief overview of the system: "This is an AI-powered todo management system that understands natural language requests"
   - Highlight key features: natural language processing, MCP tool integration, real-time visualization

2. **System Architecture Overview**
   - Mention the three-tier architecture: frontend (ChatKit), AI agent (OpenAI integration), and MCP tools
   - Emphasize the stateless, scalable design
   - Note the observability features (correlation IDs, structured logging, tool call visualization)

### Core Functionality Demo (8 minutes)

#### 1. Creating Tasks (2 minutes)
**Scenario**: User wants to add tasks to their list

**Steps**:
1. In the chat interface, type: "I need to buy groceries today"
2. Observe the agent's response: "I've added 'buy groceries today' to your task list"
3. Notice the tool call visualization showing the `add_task` MCP tool being invoked
4. Type: "Also add 'pick up kids from school' to my list"
5. Observe the second task being added

**Expected Outcome**: Two tasks are successfully added to the user's list, with tool calls visible in the UI

#### 2. Listing Tasks (2 minutes)
**Scenario**: User wants to see their current tasks

**Steps**:
1. Type: "Show me my tasks"
2. Observe the agent's response listing the tasks: "Here are your tasks: 1. buy groceries today, 2. pick up kids from school"
3. Notice the `list_tasks` MCP tool being invoked in the tool call visualization
4. Type: "What do I have scheduled for today?"
5. Observe the agent understanding the context and listing tasks

**Expected Outcome**: Tasks are retrieved and displayed, with proper tool call visualization

#### 3. Completing Tasks (2 minutes)
**Scenario**: User wants to mark tasks as completed

**Steps**:
1. Type: "I bought groceries, mark that as done"
2. Observe the agent's response: "I've marked 'buy groceries today' as completed"
3. Notice the `complete_task` MCP tool being invoked in the tool call visualization
4. Type: "Show me my tasks again"
5. Observe that the completed task is now marked as done

**Expected Outcome**: Task is marked as completed, with tool call visible in UI

#### 4. Updating Tasks (1 minute)
**Scenario**: User wants to modify an existing task

**Steps**:
1. Type: "Change 'pick up kids from school' to 'pick up kids from soccer practice'"
2. Observe the agent's response: "I've updated your task to 'pick up kids from soccer practice'"
3. Notice the `update_task` MCP tool being invoked

**Expected Outcome**: Task is updated successfully with tool call visualization

#### 5. Deleting Tasks (1 minute)
**Scenario**: User wants to remove a task

**Steps**:
1. Type: "Remove the soccer practice task"
2. Observe the agent's response: "I've removed 'pick up kids from soccer practice' from your list"
3. Notice the `delete_task` MCP tool being invoked
4. Type: "Show me my tasks"
5. Observe that the task is no longer in the list

**Expected Outcome**: Task is deleted successfully with tool call visualization

### Advanced Features Demo (5 minutes)

#### 1. Conversation Management (2 minutes)
**Scenario**: Demonstrate multi-conversation capabilities

**Steps**:
1. Show the conversation selector panel
2. Click "New Conversation" or use the new conversation button
3. In the new conversation, type: "I have a work project to do"
4. Switch back to the original conversation and verify tasks are separate
5. Demonstrate conversation naming by naming the new conversation "Work Tasks"

**Expected Outcome**: Multiple conversations maintained separately with unique task lists

#### 2. Observability Features (2 minutes)
**Scenario**: Showcase system observability

**Steps**:
1. Enable debug mode using the debug toggle in the bottom-right corner
2. Perform an action like adding a task and observe detailed logging
3. Point out the correlation IDs in the tool call visualization
4. Explain how this helps with debugging and monitoring in production
5. Show the tool call history panel if available

**Expected Outcome**: Debug information visible showing internal processes

#### 3. Error Handling (1 minute)
**Scenario**: Demonstrate system resilience

**Steps**:
1. Type an ambiguous request: "Do that thing I told you about yesterday"
2. Observe the agent's response asking for clarification
3. Type an invalid request: "Complete task number 999999999"
4. Observe the graceful error handling with a user-friendly message

**Expected Outcome**: System handles ambiguous or invalid requests gracefully

### Closing (2 minutes)

#### 1. Key Takeaways
- Natural language understanding for todo management
- MCP tool integration for database operations
- Real-time visualization of AI actions
- Multi-conversation support
- Production-ready observability and reliability features

#### 2. Q&A Preparation
- Be ready to explain the architecture in more detail
- Prepare to show code or configuration if requested
- Have answers ready for scalability and performance questions
- Be prepared to discuss security measures

## Troubleshooting Tips

### Common Issues During Demo
1. **API Key Issues**: Ensure OpenAI API key is properly configured
2. **Database Connectivity**: Verify database connection is working
3. **MCP Server Down**: Check that MCP server is running
4. **Slow Responses**: Natural language processing can take 5-10 seconds

### Verification Status Check
- Refer to `verification/runtime-checklist.md` for complete verification results
- All 24 verification checkpoints have passed successfully
- If issues arise, check component health via health check endpoints
- All security, performance, and observability features have been validated

### Backup Plans
1. Have a video recording ready in case of technical difficulties
2. Prepare screenshots of each step as fallback
3. Have a secondary environment ready if primary fails

## Expected Performance
- Response times: 3-8 seconds for typical requests
- Tool call visualization: Instantaneous feedback
- Error recovery: System should gracefully handle invalid inputs
- Concurrency: System should handle multiple simultaneous users
- All performance benchmarks verified during runtime verification

## Success Metrics
- All 5 MCP tools (add, list, complete, delete, update) demonstrated
- Natural language understanding showcased
- Tool call visualization clearly visible
- Multi-conversation features working
- Error handling demonstrated
- Observability features showcased
- All runtime verification checkpoints passed (24/24)