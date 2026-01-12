import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import { useChat } from 'ai/react';
import { useAuth } from 'better-auth/react';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  createdAt: Date;
  toolCalls?: ToolCall[];
}

interface ToolCall {
  id: string;
  toolName: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
}

export default function Home() {
  const { data: session, signOut } = useAuth();
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error,
    setInput
  } = useChat({
    api: '/api/chat',
    headers: {
      'Authorization': `Bearer ${session?.accessToken || ''}`,
      'Content-Type': 'application/json'
    },
    body: {
      user_id: session?.user.id
    },
    onError: (error) => {
      console.error('Chat error:', error);
    }
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSignOut = async () => {
    await signOut();
  };

  if (!session) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
        <Head>
          <title>Todo AI Chatbot</title>
          <meta name="description" content="AI-powered Todo Management" />
        </Head>

        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
          <h1 className="text-2xl font-bold text-center mb-4">Todo AI Chatbot</h1>
          <p className="text-gray-600 text-center mb-6">Please sign in to start managing your tasks</p>

          <button
            onClick={() => window.location.href = '/auth/signin'}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
          >
            Sign In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Head>
        <title>Todo AI Chatbot</title>
        <meta name="description" content="AI-powered Todo Management" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm py-4 px-6 flex justify-between items-center">
        <h1 className="text-xl font-semibold text-gray-800">Todo AI Chatbot</h1>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">Hello, {session.user.name}</span>
          <button
            onClick={handleSignOut}
            className="text-sm bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md transition duration-200"
          >
            Sign Out
          </button>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>

                {/* Tool call visualization if present */}
                {message.tool_calls && message.tool_calls.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-300">
                    <div className="text-xs font-semibold">Tool Calls:</div>
                    {message.tool_calls.map((toolCall: any) => (
                      <div key={toolCall.id} className="mt-1 text-xs bg-gray-300 p-2 rounded">
                        <div className="font-medium">{toolCall.function?.name}</div>
                        <div className="truncate">{toolCall.function?.arguments}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 rounded-lg p-4 max-w-[80%]">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={handleInputChange}
              placeholder="Type your message..."
              className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200 disabled:opacity-50"
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </form>

          {error && (
            <div className="mt-2 text-sm text-red-600">
              Error: {error.message}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}