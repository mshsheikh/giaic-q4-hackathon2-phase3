"""
Main entry point for the TodoAgent
"""
import asyncio
from .todo_agent import TodoAgent


async def main():
    """
    Main function to demonstrate the TodoAgent
    """
    # Create the agent
    agent = TodoAgent()

    print("TodoAgent initialized and ready to handle requests")

    # Example usage
    user_message = "Add 'buy groceries' to my todo list"
    user_id = "user123"

    print(f"\nProcessing request: {user_message}")
    result = await agent.process_request(user_message, user_id)

    print(f"Response: {result['response']}")
    print(f"Tool calls made: {len(result['tool_calls'])}")

    # Clean up
    await agent.close()


if __name__ == "__main__":
    asyncio.run(main())