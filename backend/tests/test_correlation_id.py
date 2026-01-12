"""
Unit tests for correlation ID functionality
"""
import pytest
from unittest.mock import Mock, patch
from backend.middleware.correlation_id_middleware import CorrelationIDMiddleware, get_correlation_id
from backend.utils.correlation_id_generator import (
    generate_correlation_id,
    set_correlation_id,
    get_correlation_id_from_context,
    correlation_id_context
)
from fastapi import Request
from starlette.datastructures import Headers


@pytest.fixture
def mock_request():
    """Create a mock request object for testing"""
    request = Mock(spec=Request)
    request.headers = Headers()
    request.state = Mock()
    return request


class TestCorrelationIDMiddleware:
    """Test cases for CorrelationIDMiddleware"""

    @pytest.mark.asyncio
    async def test_dispatch_with_existing_header(self, mock_request):
        """Test middleware when correlation ID header is provided"""
        correlation_id = "test-correlation-id-123"
        mock_request.headers = Headers({"X-Correlation-ID": correlation_id})

        middleware = CorrelationIDMiddleware(Mock())
        call_next = Mock()
        mock_response = Mock()
        call_next.return_value = mock_response

        response = await middleware.dispatch(mock_request, call_next)

        # Verify correlation ID was set in request state
        assert mock_request.state.correlation_id == correlation_id
        # Verify response has correlation ID header
        mock_response.headers.__setitem__.assert_called_with("X-Correlation-ID", correlation_id)
        # Verify call_next was called
        call_next.assert_called_once_with(mock_request)

    @pytest.mark.asyncio
    async def test_dispatch_without_header_generates_id(self, mock_request):
        """Test middleware generates correlation ID when none is provided"""
        mock_request.headers = Headers({})

        middleware = CorrelationIDMiddleware(Mock())
        call_next = Mock()
        mock_response = Mock()
        call_next.return_value = mock_response

        response = await middleware.dispatch(mock_request, call_next)

        # Verify correlation ID was generated and set in request state
        assert mock_request.state.correlation_id is not None
        assert len(mock_request.state.correlation_id) > 0
        # Verify response has correlation ID header
        mock_response.headers.__setitem__.assert_called_with(
            "X-Correlation-ID",
            mock_request.state.correlation_id
        )

    def test_get_correlation_id_with_state(self, mock_request):
        """Test getting correlation ID from request state"""
        expected_id = "test-id-456"
        mock_request.state.correlation_id = expected_id

        result = get_correlation_id(mock_request)

        assert result == expected_id

    def test_get_correlation_id_without_state(self, mock_request):
        """Test getting correlation ID when not in request state"""
        # Remove correlation_id attribute from state
        delattr(mock_request.state, 'correlation_id')

        result = get_correlation_id(mock_request)

        # Should generate a new ID
        assert result is not None
        assert len(result) > 0


class TestCorrelationIDGenerator:
    """Test cases for correlation ID generator utilities"""

    def test_generate_correlation_id_creates_uuid(self):
        """Test that generate_correlation_id creates valid UUIDs"""
        correlation_id = generate_correlation_id()

        # Verify it's a string and looks like a UUID
        assert isinstance(correlation_id, str)
        assert len(correlation_id) > 10  # UUIDs are quite long
        # Verify it contains hyphens which are characteristic of UUIDs
        assert '-' in correlation_id

    def test_set_and_get_correlation_id_context(self):
        """Test setting and getting correlation ID in context"""
        test_id = "test-context-id-789"

        # Set correlation ID in context
        set_correlation_id(test_id)

        # Get correlation ID from context
        result = get_correlation_id_from_context()

        assert result == test_id

    def test_correlation_id_context_manager(self):
        """Test correlation ID context manager"""
        original_id = "original-id"
        context_id = "context-id"

        # Set an original ID
        set_correlation_id(original_id)
        assert get_correlation_id_from_context() == original_id

        # Use context manager to temporarily set a different ID
        with correlation_id_context(context_id):
            assert get_correlation_id_from_context() == context_id

        # Verify original ID is restored after context
        assert get_correlation_id_from_context() == original_id

    def test_correlation_id_context_manager_nested(self):
        """Test nested correlation ID contexts"""
        outer_id = "outer-id"
        inner_id = "inner-id"

        with correlation_id_context(outer_id):
            assert get_correlation_id_from_context() == outer_id

            with correlation_id_context(inner_id):
                assert get_correlation_id_from_context() == inner_id

            assert get_correlation_id_from_context() == outer_id