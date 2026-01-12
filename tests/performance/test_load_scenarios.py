"""
Performance tests for load scenarios
"""
import pytest
import asyncio
import time
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from typing import List, Dict, Any
import statistics
from dataclasses import dataclass


@dataclass
class PerformanceResult:
    """Class to hold performance test results"""
    test_name: str
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_second: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    throughput_per_second: float


class LoadTester:
    """Load tester for performance and stress testing"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    async def single_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a single request and measure response time"""
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response_time = time.time() - start_time
            return {
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code == 200,
                "content": response.text
            }
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "status_code": 500,
                "response_time": response_time,
                "success": False,
                "error": str(e)
            }

    async def run_concurrent_requests(
        self,
        endpoint: str,
        payload_template: Dict[str, Any],
        num_requests: int,
        concurrency_level: int
    ) -> List[Dict[str, Any]]:
        """Run multiple concurrent requests"""
        start_time = time.time()

        # Create tasks for concurrent execution
        tasks = []
        for i in range(num_requests):
            # Vary the payload slightly to simulate different users
            payload = payload_template.copy()
            if "user_id" in payload:
                payload["user_id"] = f"user_{random.randint(1, 1000)}"
            if "message" in payload:
                messages = [
                    "Add 'buy groceries' to my list",
                    "Show me my tasks",
                    "Complete 'buy groceries'",
                    "Update task 'groceries' to 'buy groceries and milk'",
                    "Delete task 'buy groceries'"
                ]
                payload["message"] = random.choice(messages)

            task = self.single_request(endpoint, payload)
            tasks.append(task)

        # Execute tasks with concurrency limit
        results = []
        semaphore = asyncio.Semaphore(concurrency_level)

        async def bounded_request(task):
            async with semaphore:
                return await task

        bounded_tasks = [bounded_request(task) for task in tasks]
        results = await asyncio.gather(*bounded_tasks, return_exceptions=True)

        total_time = time.time() - start_time

        # Filter out any exceptions
        valid_results = []
        for result in results:
            if isinstance(result, dict):
                valid_results.append(result)
            else:
                # If there was an exception, create a failure result
                valid_results.append({
                    "status_code": 500,
                    "response_time": 0,
                    "success": False,
                    "error": str(result)
                })

        return valid_results, total_time

    def calculate_performance_metrics(
        self,
        results: List[Dict[str, Any]],
        total_time: float,
        num_requests: int
    ) -> PerformanceResult:
        """Calculate performance metrics from test results"""
        response_times = [r["response_time"] for r in results if isinstance(r, dict)]

        if not response_times:
            return PerformanceResult(
                test_name="default",
                avg_response_time=0,
                min_response_time=0,
                max_response_time=0,
                p95_response_time=0,
                p99_response_time=0,
                requests_per_second=0,
                total_requests=num_requests,
                successful_requests=0,
                failed_requests=num_requests,
                throughput_per_second=0
            )

        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)

        # Calculate percentiles
        sorted_times = sorted(response_times)
        n = len(sorted_times)
        p95_idx = int(0.95 * n) - 1
        p99_idx = int(0.99 * n) - 1

        p95_response_time = sorted_times[min(p95_idx, n-1)]
        p99_response_time = sorted_times[min(p99_idx, n-1)]

        successful_requests = sum(1 for r in results if r.get("success", False))
        failed_requests = num_requests - successful_requests

        requests_per_second = num_requests / total_time if total_time > 0 else 0
        throughput_per_second = successful_requests / total_time if total_time > 0 else 0

        return PerformanceResult(
            test_name="load_test",
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time,
            requests_per_second=requests_per_second,
            total_requests=num_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            throughput_per_second=throughput_per_second
        )


class TestLoadScenarios:
    """Test class for load scenarios"""

    def setup_method(self):
        """Setup for each test method"""
        self.load_tester = LoadTester(base_url="http://localhost:8000")  # Adjust as needed

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_light_load_scenario(self):
        """Test light load scenario: 10 concurrent users, 50 requests total"""
        payload_template = {
            "user_id": "user_1",
            "message": "Add 'buy groceries' to my list"
        }

        results, total_time = await self.load_tester.run_concurrent_requests(
            endpoint="/api/user_1/chat",
            payload_template=payload_template,
            num_requests=50,
            concurrency_level=10
        )

        metrics = self.load_tester.calculate_performance_metrics(results, total_time, 50)

        print(f"\nLight Load Test Results:")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  P95 Response Time: {metrics.p95_response_time:.3f}s")
        print(f"  P99 Response Time: {metrics.p99_response_time:.3f}s")
        print(f"  Requests/Second: {metrics.requests_per_second:.2f}")
        print(f"  Success Rate: {(metrics.successful_requests/metrics.total_requests)*100:.2f}%")

        # Assert performance requirements for light load
        assert metrics.p95_response_time < 5.0, f"P95 response time {metrics.p95_response_time}s exceeds 5s threshold"
        assert metrics.successful_requests >= metrics.total_requests * 0.95, "Success rate below 95%"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_medium_load_scenario(self):
        """Test medium load scenario: 50 concurrent users, 200 requests total"""
        payload_template = {
            "user_id": "user_1",
            "message": "Show me my tasks"
        }

        results, total_time = await self.load_tester.run_concurrent_requests(
            endpoint="/api/user_1/chat",
            payload_template=payload_template,
            num_requests=200,
            concurrency_level=50
        )

        metrics = self.load_tester.calculate_performance_metrics(results, total_time, 200)

        print(f"\nMedium Load Test Results:")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  P95 Response Time: {metrics.p95_response_time:.3f}s")
        print(f"  P99 Response Time: {metrics.p99_response_time:.3f}s")
        print(f"  Requests/Second: {metrics.requests_per_second:.2f}")
        print(f"  Success Rate: {(metrics.successful_requests/metrics.total_requests)*100:.2f}%")

        # Assert performance requirements for medium load
        assert metrics.p95_response_time < 8.0, f"P95 response time {metrics.p95_response_time}s exceeds 8s threshold"
        assert metrics.successful_requests >= metrics.total_requests * 0.90, "Success rate below 90%"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_heavy_load_scenario(self):
        """Test heavy load scenario: 100 concurrent users, 500 requests total"""
        payload_template = {
            "user_id": "user_1",
            "message": "Complete 'buy groceries'"
        }

        results, total_time = await self.load_tester.run_concurrent_requests(
            endpoint="/api/user_1/chat",
            payload_template=payload_template,
            num_requests=500,
            concurrency_level=100
        )

        metrics = self.load_tester.calculate_performance_metrics(results, total_time, 500)

        print(f"\nHeavy Load Test Results:")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  P95 Response Time: {metrics.p95_response_time:.3f}s")
        print(f"  P99 Response Time: {metrics.p99_response_time:.3f}s")
        print(f"  Requests/Second: {metrics.requests_per_second:.2f}")
        print(f"  Success Rate: {(metrics.successful_requests/metrics.total_requests)*100:.2f}%")

        # For heavy load, we allow slightly higher response times
        assert metrics.p95_response_time < 15.0, f"P95 response time {metrics.p95_response_time}s exceeds 15s threshold"
        assert metrics.successful_requests >= metrics.total_requests * 0.85, "Success rate below 85%"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_conversation_management_load(self):
        """Test load on conversation management endpoints"""
        # Test various conversation endpoints under load
        endpoints_and_payloads = [
            ("/conversations/", {"name": "Test Conversation", "description": "Test Description"}),
            ("/conversations/", {"name": "Another Conversation"}),
        ]

        # Cycle through different payloads
        all_results = []
        total_time_start = time.time()

        for i in range(100):  # 100 requests total
            payload_template = endpoints_and_payloads[i % len(endpoints_and_payloads)][1]
            endpoint = endpoints_and_payloads[i % len(endpoints_and_payloads)][0]

            result, _ = await self.load_tester.run_concurrent_requests(
                endpoint=endpoint,
                payload_template=payload_template,
                num_requests=1,
                concurrency_level=10  # Still allow some concurrency
            )
            all_results.extend(result)

        total_time = time.time() - total_time_start

        metrics = self.load_tester.calculate_performance_metrics(all_results, total_time, 100)

        print(f"\nConversation Management Load Test Results:")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  P95 Response Time: {metrics.p95_response_time:.3f}s")
        print(f"  P99 Response Time: {metrics.p99_response_time:.3f}s")
        print(f"  Requests/Second: {metrics.requests_per_second:.2f}")
        print(f"  Success Rate: {(metrics.successful_requests/metrics.total_requests)*100:.2f}%")

        assert metrics.p95_response_time < 10.0, f"P95 response time {metrics.p95_response_time}s exceeds 10s threshold"
        assert metrics.successful_requests >= metrics.total_requests * 0.90, "Success rate below 90%"

    def test_calculate_percentiles(self):
        """Test percentile calculation logic"""
        # Test with known values
        times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = len(times)

        # 95th percentile of 10 items should be at index int(0.95*10)-1 = 8 (0-indexed), value = 9
        p95_idx = int(0.95 * n) - 1
        p95_value = times[min(p95_idx, n-1)]

        assert p95_value == 9

        # 99th percentile of 10 items should be at index int(0.99*10)-1 = 8 (0-indexed), value = 9
        p99_idx = int(0.99 * n) - 1
        p99_value = times[min(p99_idx, n-1)]

        assert p99_value == 9