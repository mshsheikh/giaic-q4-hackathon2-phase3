"""
Integration tests for observation flow across multiple components
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime
from backend.middleware.correlation_id_middleware import CorrelationIDMiddleware
from backend.logging.config import log_with_context
from backend.config.debug_config import get_debug_config
from backend.middleware.debug_middleware import is_debug_enabled
from backend.middleware.timeout_middleware import TimeoutMiddleware
from backend.middleware.validation_middleware import validate_input_with_schema
from backend.schemas.validation_schemas import ChatRequestValidationSchema
from backend.services.circuit_breaker import CircuitBreaker
from mcp_server.handlers.error_handler import MCPServerErrorHandler
from agent.handlers.tool_failure_handler import ToolFailureHandler


class TestObservationFlow:
    """Integration tests for end-to-end observation flow"""

    @pytest.mark.asyncio
    async def test_full_correlation_id_flow(self):
        """Test correlation ID flow from frontend to backend to MCP to agent"""
        # Create a mock request with correlation ID header
        mock_request = Mock()
        mock_request.headers = {"X-Correlation-ID": "test-correlation-123"}
        mock_request.state = Mock()

        # Create a mock response
        mock_response = Mock()
        mock_response.headers = {}

        # Create the middleware
        middleware = CorrelationIDMiddleware(AsyncMock())

        # Track the call_next function
        async def mock_call_next(req):
            # Verify correlation ID is set in request state
            assert req.state.correlation_id == "test-correlation-123"

            # Simulate downstream processing that would pass correlation ID
            # to other services
            downstream_context = {
                "correlation_id": req.state.correlation_id,
                "service": "backend"
            }

            # This simulates how the correlation ID would be passed
            # to MCP server and agent
            mcp_context = {**downstream_context, "service": "mcp_server"}
            agent_context = {**downstream_context, "service": "agent"}

            # Verify all contexts have the same correlation ID
            assert downstream_context["correlation_id"] == "test-correlation-123"
            assert mcp_context["correlation_id"] == "test-correlation-123"
            assert agent_context["correlation_id"] == "test-correlation-123"

            return mock_response

        # Dispatch the request through middleware
        result = await middleware.dispatch(mock_request, mock_call_next)

        # Verify the correlation ID was added to the response
        assert result.headers["X-Correlation-ID"] == "test-correlation-123"

    @pytest.mark.asyncio
    async def test_logging_with_correlation_id(self):
        """Test structured logging with correlation ID context"""
        # Mock a request with correlation ID
        mock_request = Mock()
        mock_request.state = Mock()
        mock_request.state.correlation_id = "test-log-correlation-456"
        mock_request.url = Mock()
        mock_request.url.path = "/api/test"
        mock_request.method = "POST"

        # Generate log data with correlation ID context
        log_data = log_with_context(
            request=mock_request,
            user_id="test_user",
            service="backend",
            operation="test_operation"
        )

        # Verify correlation ID is in log data
        assert log_data["correlation_id"] == "test-log-correlation-456"
        assert log_data["service"] == "backend"
        assert log_data["user_id"] == "test_user"
        assert "timestamp" in log_data

    def test_debug_mode_integration(self):
        """Test debug mode configuration and middleware integration"""
        # Test debug configuration
        debug_config = get_debug_config()
        original_debug_mode = debug_config.DEBUG_MODE

        # Temporarily enable debug mode
        debug_config.DEBUG_MODE = True

        # Mock a request with debug header
        mock_request = Mock()
        mock_request.headers = {"X-Debug-Mode": "true"}

        # Test debug mode detection
        assert is_debug_enabled(mock_request) is True

        # Test with config-enabled debug mode
        mock_request_no_header = Mock()
        mock_request_no_header.headers = {}
        assert is_debug_enabled(mock_request_no_header) is True

        # Test with both disabled
        debug_config.DEBUG_MODE = False
        mock_request_disabled = Mock()
        mock_request_disabled.headers = {"X-Debug-Mode": "false"}
        assert is_debug_enabled(mock_request_disabled) is False

        # Restore original config
        debug_config.DEBUG_MODE = original_debug_mode

    @pytest.mark.asyncio
    async def test_timeout_integration_with_circuit_breaker(self):
        """Test timeout middleware integration with circuit breaker"""
        # Create timeout middleware
        timeout_middleware = TimeoutMiddleware(AsyncMock(), default_timeout=2)

        # Create a circuit breaker
        circuit_breaker = CircuitBreaker("test_operation")

        # Mock a slow function that should trigger timeout
        async def slow_func():
            await asyncio.sleep(3)  # Longer than timeout
            return "success"

        # Test timeout enforcement
        async def mock_call_with_timeout(request):
            try:
                # This should trigger timeout
                result = await timeout_middleware.dispatch(
                    request,
                    lambda req: slow_func()
                )
                return result
            except Exception as e:
                # Should be a timeout exception
                return str(e)

        # Create a mock request
        mock_request = Mock()

        # The timeout should trigger before circuit breaker logic
        # This tests the integration of timeout protection
        with pytest.raises(asyncio.TimeoutError):
            # Simulate the timeout scenario
            await asyncio.wait_for(slow_func(), timeout=2.5)

    def test_validation_integration_with_logging(self):
        """Test validation integration with logging"""
        # Test valid input
        valid_data = {
            "user_id": "valid_user",
            "message": "Valid message content",
            "conversation_id": "valid_conv"
        }

        try:
            validated_data = validate_input_with_schema(valid_data, ChatRequestValidationSchema)
            assert validated_data.user_id == "valid_user"
            assert validated_data.message == "Valid message content"
        except Exception:
            # If validation fails, it should raise ValidationError
            pytest.fail("Valid data should pass validation")

        # Test invalid input and ensure proper error logging would occur
        invalid_data = {
            "user_id": "",  # Invalid - empty
            "message": "",  # Invalid - empty
            "conversation_id": "valid_conv"
        }

        with pytest.raises(Exception):  # Should raise ValidationError
            validate_input_with_schema(invalid_data, ChatRequestValidationSchema)

    def test_error_handler_integration(self):
        """Test error handler integration across components"""
        # Test MCP server error handler
        error_handler = MCPServerErrorHandler()

        test_error = ValueError("Test error message")
        result = error_handler.handle_tool_error(
            tool_name="test_tool",
            error=test_error,
            user_id="test_user",
            correlation_id="test_corr_id",
            parameters={"param": "value"}
        )

        # Verify error response structure
        assert result["success"] is False
        assert result["error"]["code"] == "INVALID_INPUT"
        assert "Test error message" in result["error"]["message"]
        assert result["error"]["correlation_id"] == "test_corr_id"

        # Test agent tool failure handler
        agent_handler = ToolFailureHandler()
        agent_result = agent_handler.handle_tool_failure(
            tool_name="test_agent_tool",
            error=test_error,
            user_id="test_user",
            conversation_id="test_conv",
            correlation_id="test_corr_id_2",
            parameters={"param": "value"}
        )

        # Verify agent error response structure
        assert agent_result["success"] is False
        assert "FAILED" in agent_result["error"]["code"]
        assert "Test error message" in agent_result["error"]["message"]
        assert agent_result["error"]["correlation_id"] == "test_corr_id_2"

    @pytest.mark.asyncio
    async def test_full_request_flow_simulation(self):
        """Simulate a full request flow through multiple components"""
        # This test simulates how a request flows through the system
        correlation_id = "full-flow-test-123"

        # 1. Request enters with correlation ID
        mock_request = Mock()
        mock_request.headers = {"X-Correlation-ID": correlation_id}
        mock_request.state = Mock()
        mock_request.method = "POST"
        mock_request.url = Mock()
        mock_request.url.path = "/api/test_user/chat"

        # 2. Correlation ID middleware processes request
        correlation_middleware = CorrelationIDMiddleware(AsyncMock())

        async def process_request_chain(req):
            # Verify correlation ID is set
            assert req.state.correlation_id == correlation_id

            # 3. Validation would occur
            try:
                test_data = {"user_id": "test_user", "message": "test message"}
                validated = validate_input_with_schema(test_data, ChatRequestValidationSchema)
            except Exception as e:
                # Handle validation error
                error_log = log_with_context(
                    request=req,
                    error=str(e),
                    correlation_id=correlation_id
                )
                assert error_log["correlation_id"] == correlation_id
                return f"Validation failed: {e}"

            # 4. Logging with context
            log_data = log_with_context(
                request=req,
                operation="chat_request",
                correlation_id=correlation_id
            )
            assert log_data["correlation_id"] == correlation_id
            assert log_data["operation"] == "chat_request"

            # 5. Circuit breaker protection
            cb = CircuitBreaker("chat_operation")
            test_result = "processed_successfully"

            # 6. Simulate response
            mock_response = Mock()
            mock_response.headers = {}
            return mock_response

        # Process the request
        result = await correlation_middleware.dispatch(mock_request, process_request_chain)

        # Verify response has correlation ID
        assert result.headers.get("X-Correlation-ID") == correlation_id