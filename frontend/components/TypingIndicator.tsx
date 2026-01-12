import React from 'react';

interface TypingIndicatorProps {
  isVisible: boolean;
  className?: string;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({
  isVisible,
  className = ''
}) => {
  if (!isVisible) return null;

  return (
    <div className={`flex items-center ${className}`} aria-live="polite" aria-label="Assistant is typing">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
      <span className="ml-2 text-sm text-gray-500 sr-only">Assistant is typing</span>
    </div>
  );
};

export default TypingIndicator;