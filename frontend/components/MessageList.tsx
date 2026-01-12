import React, { useRef, useEffect } from 'react';
import { Message } from 'ai/react';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

interface ToolCall {
  id: string;
  toolName: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getRoleStyle = (role: string) => {
    switch(role) {
      case 'user':
        return 'bg-blue-500 text-white ml-auto';
      case 'assistant':
        return 'bg-gray-200 text-gray-800 mr-auto';
      case 'tool':
        return 'bg-yellow-100 text-gray-800 mr-auto italic';
      default:
        return 'bg-gray-200 text-gray-800';
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[80%] rounded-lg p-4 ${getRoleStyle(message.role)}`}
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
  );
};

export default MessageList;