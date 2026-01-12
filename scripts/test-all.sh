#!/bin/bash

# Script to run tests for all components of the Todo AI Chatbot system

set -e  # Exit immediately if a command exits with a non-zero status

echo "Running tests for Todo AI Chatbot System..."

# Test backend
echo "Testing backend..."
cd backend
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
fi
python -m pytest tests/ -v
cd ..

# Test MCP server
echo "Testing MCP server..."
cd mcp_server
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
fi
python -m pytest tests/ -v
cd ..

# Test frontend
echo "Testing frontend..."
cd frontend
npm install
npm test
cd ..

# Run integration tests if available
if [ -d "integration-tests" ]; then
    echo "Running integration tests..."
    cd integration-tests
    npm install
    npm test
    cd ..
fi

echo "All tests completed!"