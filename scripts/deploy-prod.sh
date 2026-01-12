#!/bin/bash

# Script to deploy the Todo AI Chatbot system to production environment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Deploying Todo AI Chatbot System to Production..."

# Validate that we're in the right environment
if [ "$DEPLOY_ENV" != "production" ]; then
    echo "Error: This script should only be run in production environment"
    echo "Set DEPLOY_ENV=production to proceed"
    exit 1
fi

# Build the Docker images with production tags
echo "Building production Docker images..."
docker-compose -f docker/docker-compose.prod.yml build

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker/docker-compose.prod.yml run --rm backend alembic upgrade head

# Start the services
echo "Starting production services..."
docker-compose -f docker/docker-compose.prod.yml up -d

# Wait for services to be ready
echo "Waiting for production services to be ready..."
sleep 15

# Run health checks
echo "Running production health checks..."
docker-compose -f docker-compose.prod.yml ps

echo "Production deployment completed successfully!"
echo "Services are running and available."