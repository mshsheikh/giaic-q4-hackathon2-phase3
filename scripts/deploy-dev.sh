#!/bin/bash

# Script to deploy the Todo AI Chatbot system to development environment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Deploying Todo AI Chatbot System to Development..."

# Build the Docker images
echo "Building Docker images..."
docker-compose -f docker/docker-compose.yml build

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker/docker-compose.yml run --rm backend alembic upgrade head

# Start the services
echo "Starting services..."
docker-compose -f docker/docker-compose.yml up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run tests to verify deployment
echo "Running post-deployment tests..."
./scripts/test-all.sh

echo "Development deployment completed successfully!"
echo "Services are running. Access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  MCP Server: http://localhost:8001"