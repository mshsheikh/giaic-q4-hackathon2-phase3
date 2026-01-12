# Frontend Specification: Todo AI Chatbot (ChatKit)

## Overview
This document defines the frontend specification for the Todo AI Chatbot using OpenAI ChatKit. The frontend provides a chat interface for users to interact with the TodoAgent, handling authentication, message processing, and visualization of agent actions.

## Architecture Principles
- **Stateless**: Frontend maintains no business logic or state between sessions
- **API-Driven**: Communicates exclusively with the Chat API at POST /api/{user_id}/chat
- **No Business Logic**: All task management logic resides in the backend
- **Authentication Integration**: Seamlessly integrates with Better Auth

## 1. ChatKit Configuration

### ChatKit Initialization
```javascript
import { useChat } from 'ai/react';

const TodoChatInterface = () => {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error
  } = useChat({
    api: `/api/${userId}/chat`,
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json'
    },
    body: {
      // Additional body parameters can be added here
    },
    onError: (error) => {
      // Handle errors appropriately
      console.error('Chat error:', error);
    }
  });
};
```

### Domain Allowlist Requirements
- **Development**: `localhost:[port]`, `127.0.0.1:[port]`
- **Staging**: Specific staging domain (e.g., `staging-todo-app.example.com`)
- **Production**: Production domain (e.g., `todo.example.com`)
- **Preview/PR deployments**: Dynamic domains if applicable (e.g., `*.vercel.app`)

### Domain Key Usage
- **Environment-specific keys**: Separate domain keys for dev/staging/prod environments
- **Secure storage**: Domain keys stored in environment variables, never in client-side code
- **Key rotation**: Mechanism for rotating keys without deployment

### Environment Variables
```env
# Development
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY_DEV=sk-dev-xxx
NEXT_PUBLIC_API_BASE_URL_DEV=http://localhost:3000

# Staging
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY_STAGING=sk-staging-xxx
NEXT_PUBLIC_API_BASE_URL_STAGING=https://staging.example.com

# Production
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY_PROD=sk-prod-xxx
NEXT_PUBLIC_API_BASE_URL_PROD=https://todo.example.com
```

### Local vs Production Behavior
- **Local**: Mock data for development, direct API calls to local backend
- **Production**: Real API calls, enhanced error tracking, performance monitoring
- **Feature flags**: Toggle experimental features in development vs stable features in production

## 2. Authentication Handling

### Integration with Better Auth
```javascript
import { useAuth } from '@better-auth/react';

const TodoChatPage = () => {
  const { user, signIn, signOut, isSignedIn } = useAuth();

  if (!isSignedIn) {
    return <LoginForm />;
  }

  return <TodoChatInterface userId={user?.id} authToken={user?.accessToken} />;
};
```

### User Identity Propagation
- **User ID**: Passed as path parameter in API calls (`/api/{user_id}/chat`)
- **Access Token**: Included in Authorization header
- **Session Validation**: Validate session on each API call

### Session Handling Rules
- **Automatic Refresh**: Refresh tokens automatically before expiration
- **Silent Renewal**: Renew session without user interruption when possible
- **Graceful Degradation**: Clear user data and redirect to login on session failure

### Logout and Session Expiry Behavior
- **Logout**: Clear all session data, redirect to login page
- **Session Expiry**: Detect expired sessions and prompt for re-authentication
- **Background Sync**: Periodically validate session status

## 3. Message Handling

### Sending User Messages to POST /api/{user_id}/chat
```javascript
const sendMessage = async (message) => {
  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message.content,
      conversation_id: currentConversationId
    })
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.status}`);
  }

  return response.json();
};
```

### Conversation ID Management
- **New Conversations**: Generate new conversation ID when starting fresh chat
- **Existing Conversations**: Pass existing conversation ID to continue thread
- **Storage**: Store conversation ID in component state (not persisted locally)

### Assistant Response Rendering
- **Text Display**: Render assistant responses in chat bubbles with appropriate styling
- **Markdown Support**: Support basic markdown formatting in responses
- **Code Blocks**: Properly format code snippets if returned by agent

## 4. Streaming vs Non-Streaming

### Decision: Non-Streaming Implementation
- **Choice**: Disable streaming for better control over tool call visualization
- **Rationale**:
  - Allows complete responses to be analyzed before display
  - Enables proper visualization of MCP tool calls
  - Simplifies error handling and response parsing
  - Provides better UX for tool call explanations

### UI Behavior During Agent Processing
- **Loading Indicator**: Show spinner/throbber while agent processes request
- **Input Disabled**: Disable message input during processing
- **Visual Feedback**: Clear indication that agent is thinking/responding

## 5. Tool Call Visualization

### How MCP Tool Calls Are Represented in UI
```jsx
const ToolCallVisualization = ({ toolCall }) => {
  return (
    <div className="tool-call-container">
      <div className="tool-call-header">
        <span className="tool-icon">⚙️</span>
        <span className="tool-name">{toolCall.tool_name}</span>
      </div>
      <div className="tool-parameters">
        <pre>{JSON.stringify(toolCall.parameters, null, 2)}</pre>
      </div>
      <div className="tool-result">
        <span className="result-label">Result:</span>
        <pre>{JSON.stringify(toolCall.result, null, 2)}</pre>
      </div>
    </div>
  );
};
```

### Visibility Rules
- **User-Facing Actions**: Show friendly explanations of what the agent is doing
- **Technical Details**: Hide complex technical details by default, show on demand
- **Success/Failure**: Clearly indicate success or failure of tool calls

### Friendly Explanations for Actions Taken
- **Task Creation**: "I've added 'buy groceries' to your todo list."
- **Task Completion**: "I've marked 'finish report' as completed."
- **Task Listing**: "Here are your current tasks..."

## 6. Error UI

### Network Errors
- **Visual Indicator**: Clear error message with network icon
- **Retry Option**: Button to retry the failed action
- **Offline Mode**: Graceful degradation when offline

### Backend Errors
- **Generic Message**: User-friendly error message
- **Error Code**: Technical details for debugging (optional expand)
- **Support Link**: Link to help/resources

### Tool Execution Failures
- **Actionable Message**: Explain what went wrong and possible solutions
- **Fallback Option**: Suggest alternative actions when possible
- **Logging**: Send error details to monitoring system

### Authentication Errors
- **Immediate Redirect**: Redirect to login page
- **Session Timeout**: Clear notification about session expiration
- **Secure Cleanup**: Clear all sensitive data

### Empty or Invalid Responses
- **Clarification Prompt**: Ask user to rephrase or provide more details
- **Suggestion List**: Provide common action suggestions
- **Help Option**: Link to help documentation

## 7. UX Constraints

### Loading States
- **Skeleton Screens**: Show content placeholders during loading
- **Progress Indicators**: Visual feedback for long-running operations
- **Estimated Times**: Provide rough timing estimates when possible

### Disabled Input During Agent Execution
- **Visual Cue**: Gray out input field with processing indicator
- **Placeholder Text**: Show "Agent is thinking..." or similar
- **Accessibility**: Proper ARIA labels for screen readers

### Accessibility Considerations
- **Keyboard Navigation**: Full keyboard support for all interactions
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Color Contrast**: Meet WCAG AA contrast requirements
- **Focus Management**: Proper focus handling during dynamic updates
- **Alternative Text**: Descriptive alt text for icons and images

## Component Structure

### Main Chat Component
```
TodoChatPage
├── AuthGuard (redirects if not authenticated)
├── ChatContainer
│   ├── ChatHeader (user info, settings)
│   ├── MessagesList (scrollable message history)
│   │   ├── UserMessage
│   │   ├── AssistantMessage
│   │   └── ToolCallVisualization
│   ├── TypingIndicator (shows when agent is processing)
│   ├── InputArea (message input, send button)
│   └── ErrorMessage (displays any errors)
└── Sidebar (conversation history, settings)
```

### Error Boundary Component
- Wrap critical UI sections in error boundaries
- Provide user-friendly error messages
- Include option to reload or return to safe state

## Security Considerations

### Client-Side Security
- **Input Sanitization**: Sanitize all user inputs before display
- **XSS Prevention**: Properly escape HTML content
- **Token Security**: Never log or expose auth tokens in client code

### Data Privacy
- **Local Storage**: Minimize sensitive data stored locally
- **Session Management**: Proper cleanup on logout
- **Audit Trail**: Log security-relevant events appropriately

## Performance Considerations

### Optimization Strategies
- **Code Splitting**: Lazy load chat components
- **Image Optimization**: Optimize any images used in the interface
- **Bundle Size**: Keep JavaScript bundle size minimal
- **Caching**: Implement appropriate caching strategies for static assets

### Monitoring
- **Performance Metrics**: Track loading times, response times
- **Error Tracking**: Monitor error rates and types
- **User Analytics**: Track user engagement and feature usage

## Testing Considerations

### Unit Tests
- Test authentication flow components
- Test message handling logic
- Test error boundary components

### Integration Tests
- End-to-end chat flow testing
- Authentication integration testing
- Error scenario testing

### User Acceptance Testing
- Accessibility testing with assistive technologies
- Cross-browser compatibility testing
- Mobile responsiveness testing