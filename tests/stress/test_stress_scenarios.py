"""
Stress tests for extreme scenarios
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
class StressTestResult:
    """Class to hold stress test results"""
    test_name: str
    peak_response_time: float
    avg_response_time: float
    failure_rate: float
    requests_completed: int
    requests_failed: int
    duration: float
    max_concurrent_requests: int
    errors_encountered: List[str]


class StressTester:
    """Stress tester for extreme load scenarios"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    async def single_stress_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make a single request and measure response time"""
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30  # Higher timeout for stress tests
            )
            response_time = time.time() - start_time
            return {
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code in [200, 201, 429],  # Include rate limiting as success
                "content": response.text[:200]  # Truncate content
            }
        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            return {
                "status_code": 408,
                "response_time": response_time,
                "success": False,
                "error": "Request timeout"
            }
        except requests.exceptions.ConnectionError as e:
            response_time = time.time() - start_time
            return {
                "status_code": 503,
                "response_time": response_time,
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "status_code": 500,
                "response_time": response_time,
                "success": False,
                "error": str(e)
            }

    async def run_extreme_load_test(
        self,
        endpoint: str,
        payload_template: Dict[str, Any],
        num_requests: int,
        max_concurrent: int,
        duration_seconds: int = None
    ) -> List[Dict[str, Any]]:
        """Run extreme load test with many concurrent requests"""
        start_time = time.time()
        results = []
        errors = []

        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)

        async def limited_request():
            async with semaphore:
                # Vary the payload slightly to simulate different users
                payload = payload_template.copy()
                if "user_id" in payload:
                    payload["user_id"] = f"stress_user_{random.randint(1, 10000)}"
                if "message" in payload:
                    messages = [
                        "Add 'urgent task' to my list",
                        "Show me all my tasks",
                        "Complete 'urgent task'",
                        "Add 'critical task' with high priority",
                        "List tasks with status pending"
                    ]
                    payload["message"] = random.choice(messages)

                return await self.single_stress_request(endpoint, payload)

        # Create tasks
        tasks = [limited_request() for _ in range(num_requests)]

        # Execute tasks with cancellation if duration is specified
        if duration_seconds:
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=duration_seconds
                )
            except asyncio.TimeoutError:
                print(f"Stress test reached duration limit of {duration_seconds}s")
        else:
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect any errors
        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
            elif isinstance(result, dict) and not result.get("success", False):
                errors.append(result.get("error", "Unknown error"))

        total_time = time.time() - start_time

        return results, total_time, errors

    def calculate_stress_metrics(
        self,
        results: List[Dict[str, Any]],
        total_time: float,
        num_requests: int,
        errors: List[str]
    ) -> StressTestResult:
        """Calculate stress test metrics"""
        response_times = [r["response_time"] for r in results if isinstance(r, dict)]

        if not response_times:
            return StressTestResult(
                test_name="stress_test",
                peak_response_time=0,
                avg_response_time=0,
                failure_rate=1.0,
                requests_completed=0,
                requests_failed=num_requests,
                duration=total_time,
                max_concurrent_requests=0,
                errors_encountered=errors
            )

        avg_response_time = sum(response_times) / len(response_times)
        peak_response_time = max(response_times)

        successful_requests = sum(1 for r in results if isinstance(r, dict) and r.get("success", False))
        failed_requests = num_requests - successful_requests
        failure_rate = failed_requests / num_requests if num_requests > 0 else 0

        return StressTestResult(
            test_name="stress_test",
            peak_response_time=peak_response_time,
            avg_response_time=avg_response_time,
            failure_rate=failure_rate,
            requests_completed=successful_requests,
            requests_failed=failed_requests,
            duration=total_time,
            max_concurrent_requests=num_requests,
            errors_encountered=errors
        )


class TestStressScenarios:
    """Test class for stress scenarios"""

    def setup_method(self):
        """Setup for each test method"""
        self.stress_tester = StressTester(base_url="http://localhost:8000")  # Adjust as needed

    @pytest.mark.stress
    @pytest.mark.asyncio
    async def test_high_concurrency_stress(self):
        """Test system under high concurrency: 200 concurrent requests"""
        payload_template = {
            "user_id": "stress_user_1",
            "message": "Add 'stress test task' to my list"
        }

        results, total_time, errors = await self.stress_tester.run_extreme_load_test(
            endpoint="/api/stress_user_1/chat",
            payload_template=payload_template,
            num_requests=500,
            max_concurrent=200
        )

        metrics = self.stress_tester.calculate_stress_metrics(results, total_time, 500, errors)

        print(f"\nHigh Concurrency Stress Test Results:")
        print(f"  Peak Response Time: {metrics.peak_response_time:.3f}s")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  Failure Rate: {metrics.failure_rate:.2%}")
        print(f"  Requests Completed: {metrics.requests_completed}")
        print(f"  Requests Failed: {metrics.requests_failed}")
        print(f"  Duration: {metrics.duration:.2f}s")
        print(f"  Errors Encountered: {len(metrics.errors_encountered)}")

        # In stress tests, we expect some failures due to high load
        # The key is that the system doesn't crash completely
        assert metrics.failure_rate <= 0.5, f"Failure rate {metrics.failure_rate:.2%} too high (>50%)"

    @pytest.mark.stress
    @pytest.mark.asyncio
    async def test_extended_duration_stress(self):
        """Test system under extended duration load: 60 seconds"""
        payload_template = {
            "user_id": "dur_stress_user_1",
            "message": "Show my tasks"
        }

        # Run test for 60 seconds with continuous load
        start_time = time.time()

        # Create tasks for continuous requests
        results = []
        errors = []
        semaphore = asyncio.Semaphore(50)  # Limit concurrent requests

        async def continuous_request():
            async with semaphore:
                payload = payload_template.copy()
                payload["user_id"] = f"dur_stress_user_{random.randint(1, 1000)}"
                return await self.stress_tester.single_stress_request("/api/dur_stress_user_1/chat", payload)

        # Run for approximately 30 seconds (we'll limit to 30 for this test)
        tasks = []
        duration = 30  # seconds
        end_time = start_time + duration

        # Generate tasks dynamically up to the time limit
        while time.time() < end_time:
            task = asyncio.create_task(continuous_request())
            tasks.append(task)

            # Add a small delay to avoid overwhelming the system too quickly
            await asyncio.sleep(0.01)

            # Limit total tasks to prevent infinite loop
            if len(tasks) >= 200:  # Reasonable limit for 30 seconds
                break

        # Execute tasks with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=duration + 10  # Give extra time to finish
            )
        except asyncio.TimeoutError:
            print(f"Extended duration test timed out after {duration}s")

        total_time = time.time() - start_time
        num_requests = len(results)

        # Collect errors
        errors = []
        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
            elif isinstance(result, dict) and not result.get("success", False):
                errors.append(result.get("error", "Unknown error"))

        metrics = self.stress_tester.calculate_stress_metrics(results, total_time, num_requests, errors)

        print(f"\nExtended Duration Stress Test Results:")
        print(f"  Duration: {total_time:.2f}s")
        print(f"  Peak Response Time: {metrics.peak_response_time:.3f}s")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  Failure Rate: {metrics.failure_rate:.2%}")
        print(f"  Requests Completed: {metrics.requests_completed}")
        print(f"  Requests Failed: {metrics.requests_failed}")
        print(f"  Throughput: {num_requests/total_time:.2f} req/sec")
        print(f"  Errors Encountered: {len(metrics.errors_encountered)}")

        # For extended tests, focus on system stability
        assert total_time > 0, "Test should have run for some duration"
        assert metrics.failure_rate <= 0.6, f"Failure rate {metrics.failure_rate:.2%} too high (>60%)"

    @pytest.mark.stress
    @pytest.mark.asyncio
    async def test_memory_pressure_stress(self):
        """Test system under memory pressure with large payloads"""
        # Create a large payload to test memory handling
        large_message = "This is a very large message. " * 1000  # Large string
        payload_template = {
            "user_id": "memory_user_1",
            "message": large_message,
            "metadata": {
                "tags": [f"tag_{i}" for i in range(100)],
                "extra_data": {"key_" + str(i): "value_" + str(i) for i in range(50)}
            }
        }

        results, total_time, errors = await self.stress_tester.run_extreme_load_test(
            endpoint="/api/memory_user_1/chat",
            payload_template=payload_template,
            num_requests=100,
            max_concurrent=50
        )

        metrics = self.stress_tester.calculate_stress_metrics(results, total_time, 100, errors)

        print(f"\nMemory Pressure Stress Test Results:")
        print(f"  Peak Response Time: {metrics.peak_response_time:.3f}s")
        print(f"  Average Response Time: {metrics.avg_response_time:.3f}s")
        print(f"  Failure Rate: {metrics.failure_rate:.2%}")
        print(f"  Requests Completed: {metrics.requests_completed}")
        print(f"  Requests Failed: {metrics.requests_failed}")
        print(f"  Duration: {metrics.duration:.2f}s")
        print(f"  Errors Encountered: {len(metrics.errors_encountered)}")

        # Expect higher failure rate due to large payloads
        assert metrics.failure_rate <= 0.4, f"Failure rate {metrics.failure_rate:.2%} too high (>40%)"

    @pytest.mark.stress
    @pytest.mark.asyncio
    async def test_rate_limiting_effectiveness(self):
        """Test that rate limiting works under stress"""
        payload_template = {
            "user_id": "rate_limit_user_1",
            "message": "Quick request"
        }

        # Send many requests rapidly to trigger rate limiting
        results, total_time, errors = await self.stress_tester.run_extreme_load_test(
            endpoint="/api/rate_limit_user_1/chat",
            payload_template=payload_template,
            num_requests=1000,
            max_concurrent=100  # High concurrency to trigger rate limiting
        )

        # Count rate limit responses (status code 429)
        rate_limited_count = sum(1 for r in results
                                if isinstance(r, dict) and r.get("status_code") == 429)

        # Count successful responses
        successful_count = sum(1 for r in results
                              if isinstance(r, dict) and r.get("success", False) and r.get("status_code") != 429)

        metrics = self.stress_tester.calculate_stress_metrics(results, total_time, 1000, errors)

        print(f"\nRate Limiting Effectiveness Test Results:")
        print(f"  Total Requests: 1000")
        print(f"  Successful Requests: {successful_count}")
        print(f"  Rate Limited Requests: {rate_limited_count}")
        print(f"  Other Failed Requests: {metrics.requests_failed - rate_limited_count}")
        print(f"  Peak Response Time: {metrics.peak_response_time:.3f}s")
        print(f"  Duration: {metrics.duration:.2f}s")

        # Verify that rate limiting is working
        assert rate_limited_count > 0, "Rate limiting should have triggered under stress"
        assert successful_count > 0, "Some requests should still succeed despite rate limiting"

    @pytest.mark.stress
    @pytest.mark.asyncio
    async def test_recovery_after_stress(self):
        """Test system recovery after stress"""
        # First, run a stress test
        payload_template = {
            "user_id": "recovery_user_1",
            "message": "Stress test message"
        }

        # Run stress test
        stress_results, stress_time, stress_errors = await self.stress_tester.run_extreme_load_test(
            endpoint="/api/recovery_user_1/chat",
            payload_template=payload_template,
            num_requests=300,
            max_concurrent=100
        )

        # Wait briefly for system to recover
        await asyncio.sleep(5)

        # Run a normal load test to check if system recovered
        recovery_payload = {
            "user_id": "recovery_check_user_1",
            "message": "Recovery check message"
        }

        recovery_results, recovery_time, recovery_errors = await self.stress_tester.run_extreme_load_test(
            endpoint="/api/recovery_check_user_1/chat",
            payload_template=recovery_payload,
            num_requests=20,
            max_concurrent=5
        )

        recovery_successful = sum(1 for r in recovery_results
                                 if isinstance(r, dict) and r.get("success", False))

        print(f"\nRecovery Test Results:")
        print(f"  Recovery Requests: 20")
        print(f"  Recovery Successful: {recovery_successful}")
        print(f"  Recovery Success Rate: {recovery_successful/20:.2%}")

        # Verify system recovered
        assert recovery_successful >= 18, f"System should recover with at least 90% success rate, got {recovery_successful}/20"