"""
Conversation Handler for the TodoAgent
Manages the conversation flow and state for the TodoAgent.
"""
from typing import Dict, Any, List
from .todo_agent import TodoAgent
from .response_formatter import format_response


class ConversationHandler:
    """
    Handles conversation state and management for the TodoAgent.
    """

    def __init__(self, agent: TodoAgent):
        self.agent = agent
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

    async def process_message(self, user_id: str, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Process a message in the context of a conversation.

        Args:
            user_id: ID of the user sending the message
            message: The message content
            conversation_id: ID of the conversation (creates new if None)

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        # Get or create conversation history
        if conversation_id is None:
            conversation_id = f"{user_id}_new"
            self.conversations[conversation_id] = []

        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        # Process the message with the agent
        result = await self.agent.process_request(
            user_message=message,
            user_id=user_id,
            conversation_history=self.conversations[conversation_id]
        )

        # Add the user message to the conversation history
        self.conversations[conversation_id].append({
            "role": "user",
            "content": message
        })

        # Add the agent response to the conversation history
        self.conversations[conversation_id].append({
            "role": "assistant",
            "content": result["response"]
        })

        # Format the response
        formatted_response = format_response(result)

        return {
            "conversation_id": conversation_id,
            "response": formatted_response,
            "tool_calls": result["tool_calls"]
        }

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Get the history of a specific conversation.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            List of messages in the conversation
        """
        return self.conversations.get(conversation_id, [])

    def clear_conversation(self, conversation_id: str) -> bool:
        """
        Clear a specific conversation.

        Args:
            conversation_id: ID of the conversation to clear

        Returns:
            True if conversation existed and was cleared, False otherwise
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    def get_all_conversations_for_user(self, user_id: str) -> List[str]:
        """
        Get all conversation IDs for a specific user.

        Args:
            user_id: ID of the user

        Returns:
            List of conversation IDs belonging to the user
        """
        user_conversations = []
        for conv_id in self.conversations:
            if conv_id.startswith(user_id):
                user_conversations.append(conv_id)
        return user_conversations