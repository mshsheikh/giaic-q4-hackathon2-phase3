import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

interface Conversation {
  id: string;
  name: string | null;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}

interface ConversationSelectorProps {
  userId: string;
  onSelectConversation: (conversationId: string | null) => void;
  currentConversationId: string | null;
}

const ConversationSelector: React.FC<ConversationSelectorProps> = ({
  userId,
  onSelectConversation,
  currentConversationId
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  useEffect(() => {
    fetchConversations();
  }, [userId]);

  const fetchConversations = async () => {
    if (!userId) return;

    try {
      setLoading(true);
      const response = await fetch(`/api/${userId}/conversations`);

      if (!response.ok) {
        throw new Error(`Failed to fetch conversations: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.success) {
        setConversations(data.conversations || []);
      } else {
        throw new Error(data.error?.message || 'Unknown error occurred');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      console.error('Error fetching conversations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectConversation = (conversationId: string) => {
    onSelectConversation(conversationId);
    router.push(`/chat/${conversationId}`);
  };

  const handleNewConversation = () => {
    onSelectConversation(null);
    router.push(`/chat`);
  };

  if (loading) {
    return (
      <div className="p-4">
        <div className="animate-pulse flex space-x-4">
          <div className="rounded-full bg-gray-300 h-10 w-10"></div>
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-300 rounded w-3/4"></div>
            <div className="h-4 bg-gray-300 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-red-600 text-sm">
        Error loading conversations: {error}
      </div>
    );
  }

  return (
    <div className="border-r border-gray-200 w-64 bg-gray-50 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Conversations</h2>
        <button
          onClick={handleNewConversation}
          className="mt-3 w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md text-sm transition-colors"
        >
          + New Conversation
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">
            No conversations yet
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {conversations.map((conversation) => (
              <li key={conversation.id}>
                <button
                  onClick={() => handleSelectConversation(conversation.id)}
                  className={`w-full text-left p-3 hover:bg-gray-100 transition-colors ${
                    currentConversationId === conversation.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                  }`}
                >
                  <div className="font-medium text-gray-800 truncate">
                    {conversation.name || `Conversation ${new Date(conversation.createdAt).toLocaleDateString()}`}
                  </div>
                  {conversation.description && (
                    <div className="text-xs text-gray-500 truncate mt-1">
                      {conversation.description}
                    </div>
                  )}
                  <div className="text-xs text-gray-400 mt-1">
                    {new Date(conversation.updatedAt).toLocaleString()}
                  </div>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ConversationSelector;