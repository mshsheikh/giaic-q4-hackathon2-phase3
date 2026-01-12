#!/bin/bash

# Script to build all components of the Todo AI Chatbot system

set -e  # Exit immediately if a command exits with a non-zero status

echo "Building Todo AI Chatbot System..."

# Build backend
echo "Building backend..."
cd backend
pip install -r requirements.txt
cd ..

# Build MCP server
echo "Building MCP server..."
cd mcp_server
pip install -r requirements.txt
cd ..

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Build Docker images if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "Building Docker images..."
    docker-compose -f docker/docker-compose.yml build
else
    echo "Docker Compose not found, skipping Docker build"
fi

echo "Build completed successfully!"