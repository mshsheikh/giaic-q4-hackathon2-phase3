# Todo AI Chatbot

A state-of-the-art AI-powered todo management system that understands natural language requests and manages tasks through intelligent agent interactions.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Demo Instructions](#demo-instructions-for-judges)
- [System Capabilities](#system-capabilities)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)

## Features

### Core Functionality
- **Natural Language Processing**: Understands and processes natural language requests to manage todo lists
- **Task Management**: Create, list, complete, update, and delete tasks using conversational AI
- **Multi-User Support**: Secure, isolated task management for multiple users
- **Real-time Interaction**: Immediate responses to user requests with visual feedback

### Advanced Features
- **Multi-Conversation Support**: Manage multiple conversation contexts simultaneously
- **Conversation Naming**: Assign meaningful names to conversations for easy identification
- **Tool Call Visualization**: See exactly what actions the AI agent performs in real-time
- **Debug Mode**: Toggle for detailed logging and intermediate step visibility

### Production Features
- **Observability**: End-to-end correlation IDs, structured logging, and health checks
- **Reliability**: Timeout handling, graceful error recovery, and circuit breakers
- **Security**: Input validation, rate limiting, and proper user isolation
- **Scalability**: Stateless architecture supporting horizontal scaling

## Architecture

### System Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Agent        │    │   MCP Tools     │
│   (ChatKit)     │◄──►│  (OpenAI SDK)    │◄──►│  (Database)     │
│                 │    │                  │    │                 │
│ - React UI      │    │ - Natural        │    │ - add_task      │
│ - Conversation  │    │   Language       │    │ - list_tasks    │
│   Management    │    │   Processing     │    │ - complete_task │
│ - Tool Call     │    │ - Context        │    │ - delete_task   │
│   Visualization │    │   Handling       │    │ - update_task   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: Next.js with OpenAI ChatKit
- **Agent**: OpenAI API with Function Calling
- **Backend**: FastAPI with SQLModel
- **Database**: PostgreSQL with Neon
- **Authentication**: Better Auth
- **MCP Tools**: Model Context Protocol SDK
- **Containerization**: Docker & Docker Compose

## Installation

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.9+ (for backend development)
- OpenAI API key

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd giaic-q4-hackathon2-phase3
   ```

2. Copy the environment template and configure your keys:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key and other configuration
   ```

3. Start the system using Docker Compose:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d
   ```

4. The system will be available at:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - MCP Server: http://localhost:8001

## Usage

### Basic Commands
- "Add 'buy groceries' to my list" - Creates a new task
- "Show me my tasks" - Lists all current tasks
- "Complete 'buy groceries'" - Marks task as completed
- "Update 'buy groceries' to 'buy groceries and milk'" - Modifies existing task
- "Delete 'buy groceries'" - Removes task from list

### Advanced Features
- **Conversation Management**: Use the sidebar to create, switch, and manage conversations
- **Naming Conversations**: Click "Rename" to assign meaningful names to conversations
- **Debug Mode**: Toggle the debug button in the bottom-right to see detailed processing
- **Tool Visualization**: Watch real-time tool calls as the AI processes your requests

## Demo Instructions for Judges

### Pre-Demo Setup
1. Ensure all services are running:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml ps
   ```
2. Verify the system is responsive at http://localhost:3000
3. Prepare sample user accounts if needed

### Demo Flow
1. **Opening (2 minutes)**: Introduce the system's purpose and architecture
2. **Core Functionality (8 minutes)**: Demonstrate all 5 basic operations (add, list, complete, update, delete)
3. **Advanced Features (5 minutes)**: Showcase conversation management, observability, and error handling
4. **Q&A (2 minutes)**: Address questions about architecture and implementation

### Sample Demo Prompts
- "I need to remember to call the doctor tomorrow" (add task)
- "What tasks do I have?" (list tasks)
- "I called the doctor, mark it as done" (complete task)
- "Change 'call the doctor' to 'schedule doctor appointment'" (update task)
- "Remove the doctor task" (delete task)

### Expected Outcomes
- Natural language requests processed accurately
- Tool calls visualized in real-time
- Conversations managed properly with naming
- Error handling demonstrated gracefully

## System Capabilities

### Natural Language Understanding
- Processes complex sentences and requests
- Handles ambiguous or incomplete information gracefully
- Maintains context across conversation turns
- Supports various ways to express the same intent

### Task Operations
- **Add Task**: Creates new tasks with optional descriptions and priorities
- **List Tasks**: Retrieves tasks with filtering and pagination
- **Complete Task**: Updates task status to completed
- **Update Task**: Modifies task details while preserving history
- **Delete Task**: Removes tasks permanently

### Observability Features
- **Correlation IDs**: End-to-end request tracing across services
- **Structured Logging**: JSON-formatted logs with contextual information
- **Tool Call Visualization**: Real-time display of agent actions
- **Health Checks**: Comprehensive system health monitoring
- **Debug Mode**: Detailed internal process visibility

### Reliability & Safety
- **Timeout Handling**: Configurable timeouts for all operations
- **Rate Limiting**: Protection against abuse and excessive usage
- **Circuit Breakers**: Fault isolation and graceful degradation
- **Input Validation**: Comprehensive validation and sanitization
- **Error Recovery**: Graceful handling of system failures

## Technical Details

### Database Schema
- **Task**: id, user_id, title, description, status, timestamps
- **Conversation**: id, user_id, name, description, timestamps
- **Message**: id, user_id, conversation_id, role, content, timestamps

### API Endpoints
- `POST /api/{user_id}/chat` - Main chat interface
- `GET/POST/PUT/DELETE /conversations/` - Conversation management
- `GET /health` - System health check
- `GET /health/ready` - Readiness probe
- `GET /health/live` - Liveness probe

### Security Measures
- User isolation via user_id scoping
- Input validation at all boundaries
- Rate limiting to prevent abuse
- Proper authentication and authorization
- SQL injection prevention through ORM

## Troubleshooting

### Common Issues
- **Slow Responses**: Natural language processing typically takes 3-8 seconds
- **API Key Issues**: Verify OpenAI API key is correctly configured
- **Database Connectivity**: Check database connection and credentials
- **MCP Server**: Ensure MCP tools are properly registered and accessible

### Debugging
- Enable debug mode for detailed internal logging
- Check correlation IDs for request tracing
- Review structured logs for error details
- Use health endpoints to verify system status

### Performance
- Response times: 3-8 seconds for typical requests
- Concurrency: System handles multiple simultaneous users
- Scalability: Stateless design supports horizontal scaling

---

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.