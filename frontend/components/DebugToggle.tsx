import React, { useState, useEffect } from 'react';

interface DebugToggleProps {
  onDebugChange: (enabled: boolean) => void;
  initialValue?: boolean;
}

const DebugToggle: React.FC<DebugToggleProps> = ({ onDebugChange, initialValue = false }) => {
  const [isEnabled, setIsEnabled] = useState<boolean>(initialValue);

  useEffect(() => {
    // Initialize from localStorage or prop
    const savedValue = localStorage.getItem('debugMode');
    if (savedValue !== null) {
      setIsEnabled(savedValue === 'true');
    } else {
      setIsEnabled(initialValue);
    }
  }, [initialValue]);

  useEffect(() => {
    // Notify parent component of changes
    onDebugChange(isEnabled);

    // Save to localStorage
    localStorage.setItem('debugMode', isEnabled.toString());

    // Update any relevant headers or context
    if (typeof window !== 'undefined') {
      // This could be used to update API calls with debug headers
      (window as any).__TODO_DEBUG_MODE = isEnabled;
    }
  }, [isEnabled, onDebugChange]);

  const toggleDebug = () => {
    setIsEnabled(!isEnabled);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <button
        onClick={toggleDebug}
        className={`px-4 py-2 rounded-full shadow-lg transition-colors ${
          isEnabled
            ? 'bg-red-500 hover:bg-red-600 text-white'
            : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
        }`}
        aria-label={`Debug mode ${isEnabled ? 'enabled' : 'disabled'}`}
      >
        <span className="flex items-center">
          <span className={`mr-2 ${isEnabled ? 'animate-pulse' : ''}`}>🐛</span>
          Debug {isEnabled ? 'ON' : 'OFF'}
        </span>
      </button>

      {isEnabled && (
        <div className="absolute bottom-full right-0 mb-2 w-48 bg-white shadow-lg rounded p-3 text-xs border">
          <p className="font-semibold mb-1">Debug Mode Active</p>
          <ul className="list-disc list-inside space-y-1">
            <li>Detailed logging enabled</li>
            <li>Tool calls visible</li>
            <li>Verbose output</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default DebugToggle;