'use client';

import { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

interface ToolCall {
  tool_name: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
  timestamp: string;
}

interface ChatResponse {
  success: boolean;
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
  error?: {
    code: string;
    message: string;
  };
}

export default function ChatClient() {
  const [messages, setMessages] = useState<{ id: string; content: string; role: 'user' | 'assistant'; tool_calls?: ToolCall[] }[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [userId, setUserId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Access localStorage only on the client side to initialize user ID
    if (typeof window !== 'undefined') {
      const storedUserId = window['localStorage'].getItem('user_id');
      if (storedUserId) {
        setUserId(storedUserId);
      } else {
        const newUserId = uuidv4();
        window['localStorage'].setItem('user_id', newUserId);
        setUserId(newUserId);
      }
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Fetch only runs after userId is initialized
    if (!inputValue.trim() || isLoading || !userId) {
      if (!userId) {
        console.warn('userId is not initialized yet');
      }
      return;
    }

    // Log for dev verification
    console.log('Backend URL:', process.env.NEXT_PUBLIC_BACKEND_API_URL);
    console.log('User ID:', userId);

    const userMessage = {
      id: uuidv4(),
      content: inputValue,
      role: 'user' as const,
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId,
        }),
      });

      const data: ChatResponse = await response.json();

      if (data.success) {
        if (!conversationId) {
          setConversationId(data.conversation_id);
        }

        // Add assistant message to the chat
        const assistantMessage = {
          id: uuidv4(),
          content: data.response,
          role: 'assistant' as const,
          tool_calls: data.tool_calls,
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Add error message to the chat
        const errorMessage = {
          id: uuidv4(),
          content: data.error?.message || 'An error occurred',
          role: 'assistant' as const,
        };

        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: uuidv4(),
        content: 'Failed to send message. Please try again.',
        role: 'assistant' as const,
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatToolCall = (toolCall: ToolCall) => {
    return (
      <div key={toolCall.timestamp} className="mt-2 p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="font-semibold text-sm text-blue-700 dark:text-blue-300">Tool Call: {toolCall.tool_name}</div>
        <div className="text-xs mt-1 text-gray-600 dark:text-gray-400">
          <div>Parameters:</div>
          <pre className="bg-gray-100 dark:bg-gray-800 p-2 rounded mt-1 overflow-x-auto">
            {JSON.stringify(toolCall.parameters, null, 2)}
          </pre>
        </div>
        <div className="text-xs mt-2 text-gray-600 dark:text-gray-400">
          <div>Result:</div>
          <pre className="bg-gray-100 dark:bg-gray-800 p-2 rounded mt-1 overflow-x-auto">
            {JSON.stringify(toolCall.result, null, 2)}
          </pre>
        </div>
      </div>
    );
  };

  if (!userId) {
    return (
      <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
        <header className="bg-white dark:bg-gray-800 shadow-sm py-4 px-6">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold text-gray-800 dark:text-white">Todo AI Chatbot</h1>
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Loading...
            </div>
          </div>
        </header>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            <p>Loading chat interface...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm py-4 px-6">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800 dark:text-white">Todo AI Chatbot</h1>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            User: {userId.substring(0, 8) + '...'}
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden p-4">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          <div className="flex-1 overflow-y-auto mb-4 space-y-4 bg-white dark:bg-gray-800 rounded-lg p-4 shadow-inner">
            {messages.length === 0 ? (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <p className="mb-2">Welcome to Todo AI Chatbot!</p>
                <p>Start chatting to manage your tasks with AI assistance.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`p-3 rounded-lg max-w-3xl ${
                    message.role === 'user'
                      ? 'bg-blue-100 dark:bg-blue-900/50 ml-auto self-end'
                      : 'bg-gray-100 dark:bg-gray-700 mr-auto self-start'
                  }`}
                >
                  <div className="font-medium text-xs mb-1 text-gray-600 dark:text-gray-300">
                    {message.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <div className="whitespace-pre-wrap">{message.content}</div>

                  {/* Render tool calls if present */}
                  {message.tool_calls && message.tool_calls.length > 0 && (
                    <div className="mt-2">
                      <div className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Tool Calls:</div>
                      {message.tool_calls.map(formatToolCall)}
                    </div>
                  )}
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="mt-auto">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}