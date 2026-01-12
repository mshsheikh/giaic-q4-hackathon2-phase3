import React from 'react';
import { useChat } from 'ai/react';
import { useAuth } from 'better-auth/react';
import MessageList from './MessageList';
import InputArea from './InputArea';

interface ChatInterfaceProps {
  userId: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ userId }) => {
  const { data: session } = useAuth();
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error,
    setInput
  } = useChat({
    api: `/api/${userId}/chat`,
    headers: {
      'Authorization': `Bearer ${session?.accessToken || ''}`,
      'Content-Type': 'application/json'
    },
    body: {
      user_id: userId
    },
    onError: (error) => {
      console.error('Chat error:', error);
    }
  });

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm py-4 px-6 flex justify-between items-center">
        <h1 className="text-xl font-semibold text-gray-800">Todo AI Chatbot</h1>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">Hello, {session?.user.name}</span>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-hidden flex flex-col">
        <MessageList
          messages={messages}
          isLoading={isLoading}
        />

        <InputArea
          input={input}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          error={error}
        />
      </main>
    </div>
  );
};

export default ChatInterface;