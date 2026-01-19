#!/usr/bin/env python3
"""
Live test script for backend API functionality
"""

import os
import time
import json
import asyncio
import httpx
from urllib.parse import urljoin


async def run_live_tests():
    """
    Run live tests against the backend API
    """
    # Get the backend URL from environment variable
    backend_url = os.getenv("NEXT_PUBLIC_BACKEND_API_URL", "")

    # Strip trailing /api if present
    if backend_url.endswith("/api"):
        backend_url = backend_url[:-4]

    if not backend_url:
        print("ERROR: NEXT_PUBLIC_BACKEND_API_URL environment variable not set")
        return

    # Ensure the URL ends with a slash for joining
    if not backend_url.endswith("/"):
        backend_url += "/"

    # Define test user
    test_user_id = "live-test-user-claude"

    # Store test results
    test_results = {
        "timestamp": time.time(),
        "backend_url": backend_url,
        "test_user_id": test_user_id,
        "tests": []
    }

    # Create httpx client
    async with httpx.AsyncClient(timeout=30.0) as client:

        # Test 1: GET /api/test-db
        print("Running test 1: GET /api/test-db")
        start_time = time.time()
        try:
            response = await client.get(urljoin(backend_url, "api/test-db"))
            latency = time.time() - start_time

            test_result = {
                "step": 1,
                "description": "GET /api/test-db",
                "status_code": response.status_code,
                "response_text": response.text,
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Status: {response.status_code}, Latency: {latency:.2f}s")
        except Exception as e:
            latency = time.time() - start_time
            test_result = {
                "step": 1,
                "description": "GET /api/test-db",
                "status_code": None,
                "response_text": str(e),
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Error: {e}, Latency: {latency:.2f}s")

        # Test 2: chat "hi"
        print("Running test 2: chat 'hi'")
        start_time = time.time()
        try:
            response = await client.post(
                urljoin(backend_url, f"api/chat/{test_user_id}"),
                json={"message": "hi", "conversation_id": None}
            )
            latency = time.time() - start_time

            test_result = {
                "step": 2,
                "description": "chat 'hi'",
                "status_code": response.status_code,
                "response_text": response.text,
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Status: {response.status_code}, Latency: {latency:.2f}s")
        except Exception as e:
            latency = time.time() - start_time
            test_result = {
                "step": 2,
                "description": "chat 'hi'",
                "status_code": None,
                "response_text": str(e),
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Error: {e}, Latency: {latency:.2f}s")

        # Test 3: chat "Add a task to buy test milk"
        print("Running test 3: chat 'Add a task to buy test milk'")
        start_time = time.time()
        try:
            response = await client.post(
                urljoin(backend_url, f"api/chat/{test_user_id}"),
                json={"message": "Add a task to buy test milk", "conversation_id": None}
            )
            latency = time.time() - start_time

            test_result = {
                "step": 3,
                "description": "chat 'Add a task to buy test milk'",
                "status_code": response.status_code,
                "response_text": response.text,
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Status: {response.status_code}, Latency: {latency:.2f}s")
        except Exception as e:
            latency = time.time() - start_time
            test_result = {
                "step": 3,
                "description": "chat 'Add a task to buy test milk'",
                "status_code": None,
                "response_text": str(e),
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Error: {e}, Latency: {latency:.2f}s")

        # Test 4: chat "Show me all my tasks"
        print("Running test 4: chat 'Show me all my tasks'")
        start_time = time.time()
        try:
            response = await client.post(
                urljoin(backend_url, f"api/chat/{test_user_id}"),
                json={"message": "Show me all my tasks", "conversation_id": None}
            )
            latency = time.time() - start_time

            test_result = {
                "step": 4,
                "description": "chat 'Show me all my tasks'",
                "status_code": response.status_code,
                "response_text": response.text,
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Status: {response.status_code}, Latency: {latency:.2f}s")
        except Exception as e:
            latency = time.time() - start_time
            test_result = {
                "step": 4,
                "description": "chat 'Show me all my tasks'",
                "status_code": None,
                "response_text": str(e),
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Error: {e}, Latency: {latency:.2f}s")

        # Test 5: chat "Delete the task buy test milk"
        print("Running test 5: chat 'Delete the task buy test milk'")
        start_time = time.time()
        try:
            response = await client.post(
                urljoin(backend_url, f"api/chat/{test_user_id}"),
                json={"message": "Delete the task buy test milk", "conversation_id": None}
            )
            latency = time.time() - start_time

            test_result = {
                "step": 5,
                "description": "chat 'Delete the task buy test milk'",
                "status_code": response.status_code,
                "response_text": response.text,
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Status: {response.status_code}, Latency: {latency:.2f}s")
        except Exception as e:
            latency = time.time() - start_time
            test_result = {
                "step": 5,
                "description": "chat 'Delete the task buy test milk'",
                "status_code": None,
                "response_text": str(e),
                "latency": latency
            }
            test_results["tests"].append(test_result)
            print(f"  Error: {e}, Latency: {latency:.2f}s")

    # Write results to JSON file
    output_path = "backend/backend_live_test_report.json"
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)

    print(f"\nTest results saved to: {output_path}")
    print(f"Total tests run: {len(test_results['tests'])}")


if __name__ == "__main__":
    asyncio.run(run_live_tests())