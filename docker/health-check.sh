#!/bin/bash

# Health check script for Docker containers
# This script checks the health of the service by making a request to the health endpoint

set -e

# Default values
SERVICE_URL=${HEALTH_CHECK_URL:-"http://localhost:8000/health"}
TIMEOUT=${HEALTH_CHECK_TIMEOUT:-5}
EXPECTED_STATUS=${HEALTH_CHECK_EXPECTED_STATUS:-200}

# Function to check service health
check_health() {
    local url=$1
    local timeout=$2
    local expected_status=$3

    # Use curl to check the health endpoint
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" || echo "000")

    if [ "$response_code" = "$expected_status" ]; then
        # Additional check: verify the response contains expected health status
        local health_status
        health_status=$(curl -s --max-time "$timeout" "$url" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

        if [ "$health_status" = "ok" ] || [ "$health_status" = "warning" ]; then
            echo "Health check passed: Service is healthy (status: $health_status)"
            return 0
        else
            echo "Health check failed: Service status is $health_status"
            return 1
        fi
    else
        echo "Health check failed: Expected status $expected_status, got $response_code"
        return 1
    fi
}

# Main execution
if [ $# -eq 0 ]; then
    # No arguments provided, use defaults
    if check_health "$SERVICE_URL" "$TIMEOUT" "$EXPECTED_STATUS"; then
        exit 0
    else
        exit 1
    fi
else
    # Arguments provided, use them
    if check_health "$1" "${2:-$TIMEOUT}" "${3:-$EXPECTED_STATUS}"; then
        exit 0
    else
        exit 1
    fi
fi