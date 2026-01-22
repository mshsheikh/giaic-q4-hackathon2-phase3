# Todo AI Chatbot 🤖

> **Intelligent Task Management with AI-Powered Conversations**

Transform your task management experience with an AI-powered chatbot that understands natural language and seamlessly integrates with your workflow.

## 🌟 Features

- **Conversational AI Interface** - Interact with your todo list using natural language
- **Smart Task Management** - Add, list, update, complete, and delete tasks via chat
- **Real-time Processing** - Instant responses with advanced AI reasoning
- **Secure Authentication** - Enterprise-grade security and privacy protection
- **Scalable Architecture** - Built for high availability and performance
- **MCP Integration** - Modular tool architecture supporting extensible functionality

## 🛠️ Tech Stack

![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-0056D3?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.16-29BEB0?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white)

### Backend Technologies
- **FastAPI** - High-performance web framework with automatic API documentation
- **SQLModel** - SQL database modeling with Pydantic and SQLAlchemy integration
- **PostgreSQL** - Robust, scalable database with Neon serverless support
- **OpenAI API** - Advanced language models for natural language processing
- **MCP Framework** - Modular tool architecture for extensible AI capabilities

### Frontend Technologies
- **Next.js 14+** - React framework with App Router and server-side rendering
- **TypeScript** - Type-safe JavaScript for improved developer experience
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (or Neon account)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/username/todo-ai-chatbot.git
cd todo-ai-chatbot
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd ../frontend
npm install
```

4. **Configure environment variables**
```bash
# Backend (.env)
DATABASE_URL="postgresql://user:password@localhost:5432/todo_chatbot"
OPENAI_API_KEY="your-openai-api-key"
AUTH_SECRET="your-auth-secret"
JWT_SECRET="your-jwt-secret"
```

```bash
# Frontend (.env.local)
NEXT_PUBLIC_BACKEND_API_URL="http://localhost:8000/api"
NEXT_PUBLIC_OPENAI_DOMAIN_KEY="domain_key_here"
```

5. **Start the applications**
```bash
# Terminal 1 - Start backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Start frontend
cd frontend
npm run dev
```

6. **Access the application**
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 💡 Usage Examples

### Natural Language Interactions
```
User: "Add a task to buy groceries"
Bot: "I've added the task 'buy groceries' to your list!"

User: "Show me all my tasks"
Bot: "Here are your tasks: 1. Buy groceries [pending] 2. Complete project [pending]"

User: "Mark the groceries task as done"
Bot: "I've marked 'buy groceries' as completed!"
```

### API Endpoints
- `GET /health` - Health check endpoint
- `GET /api/test` - Test endpoint for deployment verification
- `GET /api/test-db` - Database connectivity check
- `POST /api/{user_id}/chat` - Main chat interface

## 🔧 Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│    Backend       │◄──►│   PostgreSQL    │
│   (Next.js)     │    │   (FastAPI)      │    │   (Neon)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │   OpenAI API     │
                       │   (GPT-4o)       │
                       └──────────────────┘
                              │
                       ┌──────────────────┐
                       │   MCP Tools      │
                       │   (Extensible)   │
                       └──────────────────┘
```

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines
- Follow the existing code style and patterns
- Write clear, descriptive commit messages
- Update documentation as needed
- Ensure all tests pass before submitting

## 📞 Contact

For questions, support, or feedback:

- **Issues**: [GitHub Issues](https://github.com/username/todo-ai-chatbot/issues)
- **Email**: support@todoai.example.com
- **Discord**: [Join our community](https://discord.gg/todoai)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🚀 Phase IV: AI-Assisted Kubernetes Deployment

### Overview
This phase implements containerized deployment of the Todo AI Chatbot application using Kubernetes orchestration with Helm charts. The deployment leverages AI-assisted DevOps tools to streamline the containerization, packaging, and deployment process.

### Tools Used
- **Docker AI (Gordon)** - Automated Dockerfile generation and optimization
- **Minikube** - Local Kubernetes cluster for development and testing
- **Helm** - Package manager for Kubernetes applications
- **kubectl-ai** - Natural language Kubernetes operations
- **Kagent** - AI-powered Kubernetes resource analysis and optimization

### AI-Assisted Workflow
1. **Containerization**: Docker AI generates optimized multi-stage Dockerfiles for both backend (FastAPI) and frontend (Next.js) applications
2. **Orchestration**: Helm charts automate the deployment configuration with configurable parameters
3. **Operations**: kubectl-ai enables natural language interaction with Kubernetes clusters
4. **Analysis**: Kagent provides intelligent insights for cluster health and optimization

### How to Reproduce Locally
1. **Prerequisites**
   ```bash
   # Install required tools
   # Docker Desktop with WSL 2 backend (Windows)
   # Minikube
   # Helm 3.x
   # kubectl
   ```

2. **Start Minikube**
   ```bash
   minikube start --driver=docker --cpus=4 --memory=8192 --disk-size=20g
   ```

3. **Build Docker Images**
   ```bash
   # Make Docker context point to Minikube
   eval $(minikube docker-env)

   # Build backend image
   docker build -f docker/backend.Dockerfile -t todo-backend:latest .

   # Build frontend image
   docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
   ```

4. **Deploy with Helm**
   ```bash
   # Install the Helm chart
   helm install todo-app helm/todo-chart/

   # Verify deployment
   kubectl get pods
   kubectl get svc
   ```

5. **Access the Application**
   ```bash
   # Get service details
   kubectl get svc

   # Access frontend via NodePort
   minikube service todo-app-frontend --url
   ```

6. **AI-Assisted Operations**
   ```bash
   # Diagnose cluster health with AI
   kubectl-ai "check why the pods are failing or confirm healthy state"

   # Scale deployments with natural language
   kubectl-ai "scale backend deployment to 2 replicas"

   # Analyze cluster with Kagent
   kagent analyze cluster
   ```

<div align="center">

**Made with ❤️ by the Todo AI Team**

[![GitHub stars](https://img.shields.io/github/stars/username/todo-ai-chatbot?style=social)](https://github.com/username/todo-ai-chatbot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/username/todo-ai-chatbot?style=social)](https://github.com/username/todo-ai-chatbot/network/members)
[![Twitter Follow](https://img.shields.io/twitter/follow/todoai?style=social)](https://twitter.com/todoai)

</div>