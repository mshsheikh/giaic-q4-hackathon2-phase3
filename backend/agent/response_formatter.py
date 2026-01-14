"""
Response Formatter for the TodoAgent
Formats agent responses for different output formats.
"""
from typing import Dict, Any, List


def format_response(result: Dict[str, Any]) -> str:
    """
    Format the agent's response for user consumption.

    Args:
        result: The raw result from the agent's process_request method

    Returns:
        Formatted string response for the user
    """
    # Start with the agent's response
    formatted = result.get("response", "")

    # Add information about tool calls if any were made
    tool_calls = result.get("tool_calls", [])
    if tool_calls:
        formatted += "\n\nI performed the following actions:\n"
        for tool_call in tool_calls:
            tool_name = tool_call.get("tool_name", "unknown")
            result_data = tool_call.get("result", {})
            success = result_data.get("success", False)

            if success:
                if tool_name == "add_task":
                    task = result_data.get("task", {})
                    formatted += f"- Added task '{task.get('title', 'unnamed')}'\n"
                elif tool_name == "complete_task":
                    task = result_data.get("task", {})
                    formatted += f"- Completed task '{task.get('title', 'unnamed')}'\n"
                elif tool_name == "delete_task":
                    formatted += f"- Deleted task\n"
                elif tool_name == "update_task":
                    task = result_data.get("task", {})
                    formatted += f"- Updated task '{task.get('title', 'unnamed')}'\n"
                elif tool_name == "list_tasks":
                    tasks = result_data.get("tasks", [])
                    formatted += f"- Listed {len(tasks)} tasks\n"
            else:
                error = result_data.get("error", {})
                error_msg = error.get("message", "unknown error")
                formatted += f"- Attempted to {tool_name} but encountered an error: {error_msg}\n"

    return formatted.strip()


def format_tool_calls_for_display(tool_calls: List[Dict[str, Any]]) -> str:
    """
    Format tool calls for display in the UI.

    Args:
        tool_calls: List of tool call results

    Returns:
        Formatted string describing the tool calls
    """
    if not tool_calls:
        return "No tools were called."

    formatted = "Tools called:\n"
    for i, tool_call in enumerate(tool_calls, 1):
        tool_name = tool_call.get("tool_name", "unknown")
        parameters = tool_call.get("parameters", {})
        result_data = tool_call.get("result", {})

        formatted += f"{i}. {tool_name}\n"
        formatted += f"   Parameters: {parameters}\n"

        success = result_data.get("success", False)
        if success:
            formatted += "   Status: Success\n"
        else:
            error = result_data.get("error", {})
            error_msg = error.get("message", "unknown error")
            formatted += f"   Status: Failed - {error_msg}\n"

    return formatted


def format_task_details(task: Dict[str, Any]) -> str:
    """
    Format task details for display.

    Args:
        task: Task dictionary

    Returns:
        Formatted string with task details
    """
    if not task:
        return "No task data available."

    title = task.get("title", "Untitled Task")
    description = task.get("description", "No description")
    status = task.get("status", "unknown")
    task_id = task.get("id", "unknown")

    formatted = f"**{title}** (ID: {task_id})\n"
    formatted += f"Status: {status}\n"
    formatted += f"Description: {description}\n"

    return formatted