/**
 * Conversation Storage Utilities for Frontend
 */

interface ConversationData {
  id: string;
  name: string | null;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}

/**
 * Store the current conversation ID in browser storage
 */
export const storeCurrentConversation = (conversationId: string | null): void => {
  if (typeof window !== 'undefined') {
    if (conversationId) {
      localStorage.setItem('currentConversationId', conversationId);
    } else {
      localStorage.removeItem('currentConversationId');
    }
  }
};

/**
 * Retrieve the current conversation ID from browser storage
 */
export const getCurrentConversation = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('currentConversationId');
  }
  return null;
};

/**
 * Store conversation metadata in browser storage
 */
export const storeConversationMetadata = (conversation: ConversationData): void => {
  if (typeof window !== 'undefined') {
    try {
      const conversations = getAllConversationsMetadata();

      // Update or add the conversation
      const existingIndex = conversations.findIndex(c => c.id === conversation.id);
      if (existingIndex !== -1) {
        conversations[existingIndex] = conversation;
      } else {
        conversations.push(conversation);
      }

      // Keep only the most recent 50 conversations to prevent storage bloat
      const trimmedConversations = conversations.slice(-50);

      localStorage.setItem('conversationMetadata', JSON.stringify(trimmedConversations));
    } catch (error) {
      console.error('Error storing conversation metadata:', error);
    }
  }
};

/**
 * Retrieve all conversation metadata from browser storage
 */
export const getAllConversationsMetadata = (): ConversationData[] => {
  if (typeof window !== 'undefined') {
    try {
      const stored = localStorage.getItem('conversationMetadata');
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (error) {
      console.error('Error retrieving conversation metadata:', error);
    }
  }
  return [];
};

/**
 * Retrieve specific conversation metadata by ID
 */
export const getConversationMetadata = (conversationId: string): ConversationData | undefined => {
  const conversations = getAllConversationsMetadata();
  return conversations.find(c => c.id === conversationId);
};

/**
 * Remove conversation metadata from browser storage
 */
export const removeConversationMetadata = (conversationId: string): void => {
  if (typeof window !== 'undefined') {
    try {
      const conversations = getAllConversationsMetadata();
      const filtered = conversations.filter(c => c.id !== conversationId);
      localStorage.setItem('conversationMetadata', JSON.stringify(filtered));
    } catch (error) {
      console.error('Error removing conversation metadata:', error);
    }
  }
};

/**
 * Clear all conversation-related storage
 */
export const clearConversationStorage = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('currentConversationId');
    localStorage.removeItem('conversationMetadata');
  }
};

/**
 * Store temporary conversation state (before saving to backend)
 */
export const storeTemporaryConversation = (tempId: string, data: any): void => {
  if (typeof window !== 'undefined') {
    try {
      const tempConversationsStr = localStorage.getItem('temporaryConversations') || '{}';
      const tempConversations = JSON.parse(tempConversationsStr);

      tempConversations[tempId] = {
        ...data,
        lastUpdated: new Date().toISOString()
      };

      // Keep only the most recent 10 temporary conversations
      const keys = Object.keys(tempConversations);
      if (keys.length > 10) {
        // Sort by last updated and keep the 10 most recent
        const sortedKeys = keys.sort((a, b) => {
          const aTime = new Date(tempConversations[a].lastUpdated).getTime();
          const bTime = new Date(tempConversations[b].lastUpdated).getTime();
          return bTime - aTime;
        });

        const trimmedKeys = sortedKeys.slice(0, 10);
        const trimmedTempConversations: Record<string, any> = {};
        trimmedKeys.forEach(key => {
          trimmedTempConversations[key] = tempConversations[key];
        });

        localStorage.setItem('temporaryConversations', JSON.stringify(trimmedTempConversations));
      } else {
        localStorage.setItem('temporaryConversations', JSON.stringify(tempConversations));
      }
    } catch (error) {
      console.error('Error storing temporary conversation:', error);
    }
  }
};

/**
 * Retrieve temporary conversation state
 */
export const getTemporaryConversation = (tempId: string): any | null => {
  if (typeof window !== 'undefined') {
    try {
      const tempConversationsStr = localStorage.getItem('temporaryConversations') || '{}';
      const tempConversations = JSON.parse(tempConversationsStr);
      return tempConversations[tempId] || null;
    } catch (error) {
      console.error('Error retrieving temporary conversation:', error);
      return null;
    }
  }
  return null;
};

/**
 * Remove temporary conversation state
 */
export const removeTemporaryConversation = (tempId: string): void => {
  if (typeof window !== 'undefined') {
    try {
      const tempConversationsStr = localStorage.getItem('temporaryConversations') || '{}';
      const tempConversations = JSON.parse(tempConversationsStr);

      delete tempConversations[tempId];
      localStorage.setItem('temporaryConversations', JSON.stringify(tempConversations));
    } catch (error) {
      console.error('Error removing temporary conversation:', error);
    }
  }
};

/**
 * Sync conversation state with backend
 * This function would typically be called periodically or when leaving the page
 */
export const syncConversationWithBackend = async (
  userId: string,
  conversationId: string,
  authToken: string
): Promise<boolean> => {
  try {
    // This would contain logic to sync any locally cached conversation data with the backend
    // For now, it just verifies that the conversation exists on the backend
    const response = await fetch(`/api/${userId}/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    });

    return response.ok;
  } catch (error) {
    console.error('Error syncing conversation with backend:', error);
    return false;
  }
};