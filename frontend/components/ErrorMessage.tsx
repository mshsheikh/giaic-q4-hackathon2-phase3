import React from 'react';

interface ErrorMessageProps {
  error: string | null;
  type?: 'network' | 'backend' | 'tool' | 'auth' | 'validation' | 'generic';
  action?: () => void;
  actionLabel?: string;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({
  error,
  type = 'generic',
  action,
  actionLabel = 'Retry',
  className = ''
}) => {
  if (!error) return null;

  // Determine error styling based on type
  const getErrorStyles = () => {
    switch (type) {
      case 'network':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'auth':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'tool':
        return 'bg-orange-50 border-orange-200 text-orange-800';
      case 'validation':
        return 'bg-purple-50 border-purple-200 text-purple-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  // Determine error title based on type
  const getErrorTitle = () => {
    switch (type) {
      case 'network':
        return 'Network Error';
      case 'auth':
        return 'Authentication Error';
      case 'tool':
        return 'Tool Execution Error';
      case 'validation':
        return 'Validation Error';
      default:
        return 'Error';
    }
  };

  return (
    <div className={`border rounded-md p-4 mb-4 ${getErrorStyles()} ${className}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium">{getErrorTitle()}</h3>
          <p className="mt-1 text-sm">{error}</p>
        </div>
        {action && (
          <button
            onClick={action}
            className={`ml-4 px-3 py-1 text-sm rounded ${
              type === 'network'
                ? 'bg-yellow-600 text-white hover:bg-yellow-700'
                : type === 'auth'
                ? 'bg-red-600 text-white hover:bg-red-700'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {actionLabel}
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;