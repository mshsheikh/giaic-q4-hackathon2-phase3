import React from 'react';

interface DisabledInputOverlayProps {
  isActive: boolean;
  message?: string;
  className?: string;
}

const DisabledInputOverlay: React.FC<DisabledInputOverlayProps> = ({
  isActive,
  message = 'Agent is processing your request...',
  className = ''
}) => {
  if (!isActive) return null;

  return (
    <div
      className={`absolute inset-0 bg-black bg-opacity-20 flex items-center justify-center z-10 ${className}`}
      aria-hidden={!isActive}
      role="alert"
    >
      <div className="bg-white p-4 rounded-md shadow-lg flex items-center">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
        <span className="text-gray-700">{message}</span>
      </div>
    </div>
  );
};

export default DisabledInputOverlay;