# Todo AI Chatbot - Quick Start Guide for Demo Environment

## Overview
This guide provides step-by-step instructions to quickly set up and run the Todo AI Chatbot system for demonstration purposes. The setup process is designed to be simple and fast, enabling rapid deployment for demos and evaluations.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Internet Connection**: Required for pulling images and API access

### Minimum Resources
- **CPU**: 2 cores or higher
- **RAM**: 8 GB or higher
- **Disk Space**: 5 GB available space

### Required Credentials
- **OpenAI API Key**: Required for AI functionality
- **PostgreSQL**: No additional setup required (uses embedded database)

## Quick Setup Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/giaic-q4-hackathon2-phase3.git
cd giaic-q4-hackathon2-phase3
```

### Step 2: Configure Environment
```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file to add your OpenAI API key
nano .env
# OR
vim .env
```

In the `.env` file, set your OpenAI API key:
```
OPENAI_API_KEY=sk-...
```

### Step 3: Start the System
```bash
# Navigate to the docker directory
cd docker

# Start all services using Docker Compose
docker-compose -f docker-compose.demo.yml up -d
```

If you don't have a specific demo compose file, use the dev configuration:
```bash
cd ..
docker-compose -f docker/docker-compose.dev.yml up -d
```

### Step 4: Verify Installation
```bash
# Check if all services are running
docker-compose -f docker/docker-compose.dev.yml ps

# Verify system health
curl http://localhost:8000/health
```

### Step 5: Access the System
- **Frontend**: Open http://localhost:3000 in your browser
- **Backend API**: Available at http://localhost:8000
- **MCP Server**: Available at http://localhost:8001

## Demo Preparation Checklist

### Before Starting Demo
- [ ] All services are running (`docker-compose ps`)
- [ ] Frontend is accessible at http://localhost:3000
- [ ] API endpoints are responding
- [ ] OpenAI API key is properly configured
- [ ] Database connection is established
- [ ] Sample data is loaded (if needed)

### Recommended Demo Flow
1. **System Overview** (2 minutes)
   - Explain the architecture and components
   - Highlight the natural language processing capabilities

2. **Basic Operations** (5 minutes)
   - Add a task: "Remember to call the doctor"
   - List tasks: "Show me my tasks"
   - Complete task: "I called the doctor, mark it as done"

3. **Advanced Features** (3 minutes)
   - Create a new conversation
   - Demonstrate tool call visualization
   - Show debug mode capabilities

## Common Demo Scenarios

### Scenario 1: Basic Task Management
```
User: "Add 'buy groceries' to my list"
AI: "I've added 'buy groceries' to your task list"

User: "Show me my tasks"
AI: "Here are your current tasks: 1. buy groceries"

User: "Complete 'buy groceries'"
AI: "I've marked 'buy groceries' as completed"
```

### Scenario 2: Conversation Management
```
User: [Click "New Conversation"]
User: "I have work tasks to manage"
AI: "I've added 'I have work tasks to manage' to your task list"

User: [Switch back to previous conversation]
User: "What were we talking about?"
AI: "Here are your current tasks: 1. buy groceries"
```

## Troubleshooting Quick Fixes

### Service Not Starting
```bash
# Stop all services
docker-compose -f docker/docker-compose.dev.yml down

# Remove any conflicting containers
docker-compose -f docker/docker-compose.dev.yml rm -f

# Start services again
docker-compose -f docker/docker-compose.dev.yml up -d
```

### Frontend Not Loading
1. Check if frontend service is running: `docker-compose ps`
2. Verify port 3000 is available: `netstat -tulpn | grep 3000`
3. Clear browser cache and hard refresh (Ctrl+Shift+R)

### API Connection Issues
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check if the OpenAI API key is properly set in `.env`
3. Confirm internet connectivity

### Slow Response Times
- Natural language processing typically takes 3-8 seconds
- First requests may be slower due to cold starts
- Subsequent requests should be faster

## Performance Optimization Tips

### For Demo Day
- Start services 15 minutes before the demo
- Test all major functionality beforehand
- Have backup screenshots ready
- Prepare a video recording as alternative

### Resource Management
- Close unnecessary applications to free up RAM
- Ensure sufficient disk space is available
- Monitor system resources during demo

## Cleanup

### After Demo
```bash
# Stop all services
docker-compose -f docker/docker-compose.dev.yml down

# Remove containers (optional)
docker-compose -f docker/docker-compose.dev.yml down -v

# Clean up unused Docker resources
docker system prune -f
```

### Complete Reset
```bash
# Remove all containers, networks, and volumes
docker-compose -f docker/docker-compose.dev.yml down -v --remove-orphans

# Clean up everything
docker system prune -a --volumes
```

## Expected Timings
- **Setup Time**: 5-10 minutes for initial installation
- **Startup Time**: 2-3 minutes for all services to be ready
- **Response Time**: 3-8 seconds for typical requests
- **Demo Duration**: 10-15 minutes for complete feature showcase

## Success Indicators
- All 3 services (frontend, backend, MCP server) running
- Green health check at http://localhost:8000/health
- Frontend accessible at http://localhost:3000
- Natural language requests processed successfully
- Tool calls visualized in real-time
- Multi-conversation features working properly

## Quick Reference Commands

### Service Management
```bash
# Start services
docker-compose -f docker/docker-compose.dev.yml up -d

# Stop services
docker-compose -f docker/docker-compose.dev.yml down

# View logs
docker-compose -f docker/docker-compose.dev.yml logs -f

# Check status
docker-compose -f docker/docker-compose.dev.yml ps
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# MCP Server health (if available)
curl http://localhost:8001/health
```