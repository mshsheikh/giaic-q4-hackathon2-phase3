# Todo AI Chatbot - Sample Prompts Collection

## Overview
This collection provides curated example inputs that demonstrate the Todo AI Chatbot system's capabilities. These prompts showcase the system's ability to understand natural language and manage todo lists through various types of requests.

## Basic Task Management

### Adding Tasks
```
Input: "I need to buy milk and bread from the grocery store"
Output: "I've added 'buy milk and bread from the grocery store' to your task list"
```

```
Input: "Add 'finish the report' to my tasks"
Output: "I've added 'finish the report' to your task list"
```

```
Input: "Don't forget to call mom tomorrow"
Output: "I've added 'call mom tomorrow' to your task list"
```

```
Input: "Schedule dentist appointment for next week"
Output: "I've added 'schedule dentist appointment for next week' to your task list"
```

### Listing Tasks
```
Input: "Show me my tasks"
Output: "Here are your current tasks: 1. buy milk and bread from the grocery store, 2. finish the report, 3. call mom tomorrow"
```

```
Input: "What do I have to do today?"
Output: "Here are your tasks for today: 1. call mom tomorrow"
```

```
Input: "What's on my todo list?"
Output: "Here are your current tasks: 1. buy milk and bread from the grocery store, 2. finish the report, 3. call mom tomorrow"
```

### Completing Tasks
```
Input: "I finished the report, mark it as done"
Output: "I've marked 'finish the report' as completed"
```

```
Input: "Complete the task about calling mom"
Output: "I've marked 'call mom tomorrow' as completed"
```

```
Input: "I bought the groceries, check that off my list"
Output: "I've marked 'buy milk and bread from the grocery store' as completed"
```

### Updating Tasks
```
Input: "Change 'call mom tomorrow' to 'call mom and dad tomorrow afternoon'"
Output: "I've updated your task to 'call mom and dad tomorrow afternoon'"
```

```
Input: "Update the dentist appointment to next Friday"
Output: "I've updated your task to 'schedule dentist appointment for next Friday'"
```

```
Input: "Change the grocery task to include eggs"
Output: "I've updated your task to 'buy milk, bread, and eggs from the grocery store'"
```

### Deleting Tasks
```
Input: "Remove the dentist appointment task"
Output: "I've removed 'schedule dentist appointment for next Friday' from your list"
```

```
Input: "Delete the task about calling mom"
Output: "I've removed 'call mom and dad tomorrow afternoon' from your list"
```

```
Input: "Cancel the report task"
Output: "I've removed 'finish the report' from your list"
```

## Advanced Task Management

### Prioritizing Tasks
```
Input: "Mark buying groceries as high priority"
Output: "I've updated 'buy milk, bread, and eggs from the grocery store' with high priority"
```

```
Input: "This report is urgent, prioritize it"
Output: "I've added 'urgent report' to your task list with high priority"
```

### Filtering Tasks
```
Input: "Show me only pending tasks"
Output: "Here are your pending tasks: 1. buy milk, bread, and eggs from the grocery store"
```

```
Input: "What tasks are completed?"
Output: "Here are your completed tasks: 1. finish the report, 2. call mom and dad tomorrow afternoon"
```

### Setting Reminders
```
Input: "Remind me about the groceries tomorrow morning"
Output: "I've added a reminder for 'buy milk, bread, and eggs from the grocery store' for tomorrow morning"
```

```
Input: "Set a reminder to call dad next Tuesday"
Output: "I've added a reminder for 'call dad' for next Tuesday"
```

## Natural Language Variations

### Casual Language
```
Input: "Hey, can you put 'walk the dog' on my list?"
Output: "I've added 'walk the dog' to your task list"
```

```
Input: "Oh, I forgot to add 'pay electricity bill' to my tasks"
Output: "I've added 'pay electricity bill' to your task list"
```

### Formal Language
```
Input: "Please add 'submit quarterly budget proposal' to my tasks"
Output: "I've added 'submit quarterly budget proposal' to your task list"
```

```
Input: "Could you remove 'attend team meeting' from my todo list?"
Output: "I've removed 'attend team meeting' from your list"
```

### Complex Sentences
```
Input: "When you get a chance, I'd like to add 'research vacation destinations' to my list of things to do"
Output: "I've added 'research vacation destinations' to your task list"
```

```
Input: "I've been thinking, maybe you could remove 'organize garage sale' from my tasks since I decided not to do it"
Output: "I've removed 'organize garage sale' from your list"
```

## Edge Cases and Error Handling

### Ambiguous Requests
```
Input: "Do that thing I mentioned before"
Output: "I'm not sure which task you're referring to. Could you please specify which task you'd like me to help with?"
```

```
Input: "Complete task #5"
Output: "I don't see a task with that number in your list. Would you like me to show you your current tasks?"
```

### Missing Information
```
Input: "Update the task"
Output: "I need more information to update your task. Could you please specify which task and how you'd like to update it?"
```

```
Input: "Remove it"
Output: "I need more information to remove a task. Could you please specify which task you'd like to remove?"
```

## Multi-step Interactions

### Conversation Flow
```
User: "I need to schedule a meeting with the marketing team"
AI: "I've added 'schedule a meeting with the marketing team' to your task list. When would you like to schedule this meeting?"

User: "Some time next week would be good"
AI: "I've updated your task to 'schedule a meeting with the marketing team for next week'. Is there anything else you'd like to add?"

User: "Yes, remind me to prepare the presentation"
AI: "I've added 'remind me to prepare the presentation' to your task list."
```

### Context Understanding
```
User: "I have to book a flight to New York"
AI: "I've added 'book a flight to New York' to your task list. When do you plan to travel?"

User: "Next month"
AI: "I've updated your task to 'book a flight to New York next month'. Would you like to set a reminder for this?"

User: "Yes, remind me two weeks before"
AI: "I've added a reminder for 'book a flight to New York' for two weeks before your planned travel date."
```

## System Capabilities Showcase

### Tool Call Visualization
- Each interaction triggers visible MCP tool calls in the UI
- `add_task` for adding new items
- `list_tasks` for retrieving current tasks
- `complete_task` for marking tasks as done
- `update_task` for modifying existing tasks
- `delete_task` for removing tasks

### Error Handling
- Graceful responses to ambiguous requests
- Helpful suggestions when information is missing
- Clear explanations when tasks are not found
- User-friendly messages for all error conditions

## Performance Benchmarks
- Response time: Under 5 seconds for most requests
- Accuracy: High success rate for natural language interpretation
- Robustness: Handles ambiguous requests gracefully
- Consistency: Reliable responses across multiple interactions