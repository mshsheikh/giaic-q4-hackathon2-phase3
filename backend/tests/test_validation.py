"""
Unit tests for validation functionality
"""
import pytest
from pydantic import ValidationError
from schemas.validation_schemas import (
    UserIdValidationSchema,
    TaskValidationSchema,
    ConversationValidationSchema,
    MessageValidationSchema,
    ChatRequestValidationSchema,
    ToolCallValidationSchema,
    PaginationValidationSchema,
    SearchValidationSchema
)


class TestUserIdValidationSchema:
    """Test cases for UserIdValidationSchema"""

    def test_valid_user_id(self):
        """Test validation with valid user ID"""
        data = {"user_id": "user123"}
        schema = UserIdValidationSchema(**data)

        assert schema.user_id == "user_id"

    def test_invalid_user_id_special_chars(self):
        """Test validation with invalid user ID containing special chars"""
        with pytest.raises(ValidationError):
            UserIdValidationSchema(user_id="user@invalid!")

    def test_empty_user_id(self):
        """Test validation with empty user ID"""
        with pytest.raises(ValidationError):
            UserIdValidationSchema(user_id="")

    def test_whitespace_only_user_id(self):
        """Test validation with whitespace-only user ID"""
        with pytest.raises(ValueError):
            UserIdValidationSchema(user_id="   ")


class TestTaskValidationSchema:
    """Test cases for TaskValidationSchema"""

    def test_valid_task(self):
        """Test validation with valid task data"""
        data = {
            "user_id": "user123",
            "title": "Test task",
            "description": "Test description",
            "status": "pending"
        }
        schema = TaskValidationSchema(**data)

        assert schema.user_id == "user_id"
        assert schema.title == "Test task"
        assert schema.description == "Test description"
        assert schema.status == "pending"

    def test_task_without_optional_fields(self):
        """Test validation with minimal required fields"""
        data = {
            "user_id": "user123",
            "title": "Test task"
        }
        schema = TaskValidationSchema(**data)

        assert schema.user_id == "user_id"
        assert schema.title == "Test task"
        assert schema.description is None
        assert schema.status is None

    def test_invalid_status(self):
        """Test validation with invalid status"""
        data = {
            "user_id": "user123",
            "title": "Test task",
            "status": "invalid_status"
        }
        with pytest.raises(ValidationError):
            TaskValidationSchema(**data)

    def test_empty_title(self):
        """Test validation with empty title"""
        data = {
            "user_id": "user123",
            "title": ""
        }
        with pytest.raises(ValidationError):
            TaskValidationSchema(**data)

    def test_whitespace_title(self):
        """Test validation with whitespace-only title"""
        data = {
            "user_id": "user123",
            "title": "   "
        }
        with pytest.raises(ValidationError):
            TaskValidationSchema(**data)


class TestPaginationValidationSchema:
    """Test cases for PaginationValidationSchema"""

    def test_valid_pagination(self):
        """Test validation with valid pagination values"""
        data = {
            "user_id": "user123",
            "limit": 10,
            "offset": 0
        }
        # Since this extends UserIdValidationSchema, we need to include user_id
        schema = type('CombinedSchema', (UserIdValidationSchema, PaginationValidationSchema), {})(**data)

        assert schema.limit == 10
        assert schema.offset == 0

    def test_invalid_limit_negative(self):
        """Test validation with negative limit"""
        data = {
            "user_id": "user123",
            "limit": -5
        }
        with pytest.raises(ValidationError):
            type('CombinedSchema', (UserIdValidationSchema, PaginationValidationSchema), {})(**data)

    def test_invalid_offset_negative(self):
        """Test validation with negative offset"""
        data = {
            "user_id": "user123",
            "offset": -5
        }
        with pytest.raises(ValidationError):
            type('CombinedSchema', (UserIdValidationSchema, PaginationValidationSchema), {})(**data)

    def test_limit_exceeds_maximum(self):
        """Test validation with limit exceeding maximum"""
        data = {
            "user_id": "user123",
            "limit": 1001  # Maximum is 1000
        }
        with pytest.raises(ValidationError):
            type('CombinedSchema', (UserIdValidationSchema, PaginationValidationSchema), {})(**data)


class TestChatRequestValidationSchema:
    """Test cases for ChatRequestValidationSchema"""

    def test_valid_chat_request(self):
        """Test validation with valid chat request"""
        data = {
            "user_id": "user123",
            "message": "Hello, world!",
            "conversation_id": "conv123"
        }
        schema = ChatRequestValidationSchema(**data)

        assert schema.user_id == "user123"
        assert schema.message == "Hello, world!"
        assert schema.conversation_id == "conv123"

    def test_invalid_empty_message(self):
        """Test validation with empty message"""
        data = {
            "user_id": "user123",
            "message": "",
            "conversation_id": "conv123"
        }
        with pytest.raises(ValidationError):
            ChatRequestValidationSchema(**data)

    def test_invalid_whitespace_message(self):
        """Test validation with whitespace-only message"""
        data = {
            "user_id": "user123",
            "message": "   ",
            "conversation_id": "conv123"
        }
        with pytest.raises(ValidationError):
            ChatRequestValidationSchema(**data)

    def test_message_exceeds_length(self):
        """Test validation with message exceeding length limit"""
        data = {
            "user_id": "user123",
            "message": "a" * 5001,  # Maximum is 5000
            "conversation_id": "conv123"
        }
        with pytest.raises(ValidationError):
            ChatRequestValidationSchema(**data)


class TestToolCallValidationSchema:
    """Test cases for ToolCallValidationSchema"""

    def test_valid_tool_call(self):
        """Test validation with valid tool call"""
        data = {
            "tool_name": "add_task",
            "parameters": {"arg1": "value1"}
        }
        schema = ToolCallValidationSchema(**data)

        assert schema.tool_name == "add_task"
        assert schema.parameters == {"arg1": "value1"}

    def test_invalid_tool_name_with_spaces(self):
        """Test validation with invalid tool name containing spaces"""
        data = {
            "tool_name": "add task",  # Contains space
            "parameters": {"arg1": "value1"}
        }
        with pytest.raises(ValidationError):
            ToolCallValidationSchema(**data)

    def test_valid_tool_name_with_special_chars(self):
        """Test validation with valid tool name containing allowed special chars"""
        data = {
            "tool_name": "add_task_v2.api",
            "parameters": {"arg1": "value1"}
        }
        schema = ToolCallValidationSchema(**data)

        assert schema.tool_name == "add_task_v2.api"