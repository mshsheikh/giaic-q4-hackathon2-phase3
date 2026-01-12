import React from 'react';

interface NewConversationButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const NewConversationButton: React.FC<NewConversationButtonProps> = ({
  onClick,
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        flex items-center justify-center space-x-2
        px-4 py-2 rounded-lg font-medium
        transition-all duration-200
        ${disabled
          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
          : 'bg-blue-500 hover:bg-blue-600 text-white hover:shadow-md'
        }
      `}
      title="Start a new conversation"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-5 w-5"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
          clipRule="evenodd"
        />
      </svg>
      <span>New Conversation</span>
    </button>
  );
};

export default NewConversationButton;