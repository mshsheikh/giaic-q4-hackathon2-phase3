import React, { useState } from 'react';

interface ConversationControlsProps {
  conversationId: string | null;
  onNewConversation: () => void;
  onResetConversation: () => void;
  onDeleteConversation: () => void;
  onRenameConversation: (name: string) => void;
}

const ConversationControls: React.FC<ConversationControlsProps> = ({
  conversationId,
  onNewConversation,
  onResetConversation,
  onDeleteConversation,
  onRenameConversation
}) => {
  const [isRenaming, setIsRenaming] = useState<boolean>(false);
  const [newName, setNewName] = useState<string>('');

  const handleRenameSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newName.trim()) {
      onRenameConversation(newName.trim());
      setIsRenaming(false);
      setNewName('');
    }
  };

  return (
    <div className="flex flex-wrap gap-2 p-3 bg-gray-100 border-t border-gray-200">
      <button
        onClick={onNewConversation}
        className="px-3 py-1.5 bg-green-500 hover:bg-green-600 text-white text-sm rounded-md transition-colors"
        title="Start new conversation"
      >
        New
      </button>

      {conversationId && (
        <>
          <button
            onClick={onResetConversation}
            className="px-3 py-1.5 bg-yellow-500 hover:bg-yellow-600 text-white text-sm rounded-md transition-colors"
            title="Reset conversation (clear messages)"
          >
            Reset
          </button>

          <button
            onClick={onDeleteConversation}
            className="px-3 py-1.5 bg-red-500 hover:bg-red-600 text-white text-sm rounded-md transition-colors"
            title="Delete conversation"
          >
            Delete
          </button>

          {!isRenaming ? (
            <button
              onClick={() => {
                setIsRenaming(true);
                setNewName(document.querySelector('.conversation-title')?.textContent || '');
              }}
              className="px-3 py-1.5 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-md transition-colors"
              title="Rename conversation"
            >
              Rename
            </button>
          ) : (
            <form onSubmit={handleRenameSubmit} className="flex gap-1">
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="Conversation name"
                className="px-2 py-1 text-sm border rounded-md"
                autoFocus
                maxLength={255}
                onKeyDown={(e) => {
                  if (e.key === 'Escape') {
                    setIsRenaming(false);
                    setNewName('');
                  }
                }}
              />
              <button
                type="submit"
                className="px-2 py-1 bg-green-500 hover:bg-green-600 text-white text-sm rounded-md"
              >
                Save
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsRenaming(false);
                  setNewName('');
                }}
                className="px-2 py-1 bg-gray-500 hover:bg-gray-600 text-white text-sm rounded-md"
              >
                Cancel
              </button>
            </form>
          )}
        </>
      )}

      {conversationId && (
        <div className="ml-auto text-sm text-gray-600 italic">
          Conversation ID: {conversationId.substring(0, 8)}...
        </div>
      )}
    </div>
  );
};

export default ConversationControls;