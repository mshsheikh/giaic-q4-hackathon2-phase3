# TodoAgent - AI-Powered Todo Management Agent

## Overview
TodoAgent is an AI-powered assistant designed to manage user todo lists through natural language interactions. The agent uses OpenAI's Agents SDK and exclusively relies on MCP (Model Context Protocol) tools for all task operations, ensuring a stateless, scalable solution.

## Core Identity
- **Name**: TodoAgent
- **Purpose**: Manage user todo lists via natural language
- **Architecture**: Stateless, tool-based agent using OpenAI Agents SDK

## MCP Tool Integration
The agent exclusively uses the following MCP tools for all operations:

- **add_task**: Create new todo items
- **list_tasks**: Retrieve and display existing tasks
- **complete_task**: Mark tasks as completed
- **delete_task**: Remove tasks from the list
- **update_task**: Modify existing task details

## Functional Capabilities

### 1. Task Creation
- Interpret natural language requests to create new tasks
- Extract task details and priority information
- Confirm successful task creation with user-friendly messages

### 2. Task Management
- Display current task lists with clear formatting
- Handle requests to mark tasks as complete
- Support multi-step operations (e.g., "Complete task A and add task B")
- Allow task updates and deletions

### 3. Conversation Handling
- Process conversation history to understand context
- Handle references to previously mentioned tasks
- Maintain context within a single conversation session

## Technical Constraints

### State Management
- Agent is stateless between conversation sessions
- Relies solely on provided conversation history
- No persistent internal state storage

### Data Access
- No direct database access
- All data operations through MCP tools only
- Works with stateless FastAPI backend

### Error Handling
- Graceful error handling without exposing internals
- User-friendly error messages
- Fallback responses when tools fail

## User Interaction Patterns

### Natural Language Processing
- Interpret various ways users express task operations
- Handle complex requests involving multiple operations
- Maintain conversation context for follow-up requests

### Response Format
- Confirm all successful operations in friendly language
- Provide clear feedback for error conditions
- Format task lists in an easily readable manner

## Implementation Requirements

### Architecture
- Built using OpenAI Agents SDK
- Stateless design pattern
- MCP tool-only data operations
- Integration with FastAPI backend

### Quality Standards
- Multi-step tool chaining support
- 95% accuracy in task operation interpretation
- Sub-5 second response times
- Comprehensive error handling