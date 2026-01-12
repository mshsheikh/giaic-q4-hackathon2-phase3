import { useState, useCallback } from 'react';

interface ErrorState {
  message: string | null;
  type: 'network' | 'backend' | 'tool' | 'auth' | 'validation' | 'generic' | null;
  timestamp: Date | null;
}

interface UseErrorHandlerReturn {
  error: ErrorState;
  showError: (message: string, type?: ErrorState['type']) => void;
  hideError: () => void;
  setError: (error: ErrorState) => void;
  clearError: () => void;
}

const useErrorHandler = (): UseErrorHandlerReturn => {
  const [error, setErrorState] = useState<ErrorState>({
    message: null,
    type: null,
    timestamp: null
  });

  const showError = useCallback((message: string, type: ErrorState['type'] = 'generic') => {
    setErrorState({
      message,
      type,
      timestamp: new Date()
    });
  }, []);

  const hideError = useCallback(() => {
    setErrorState({
      message: null,
      type: null,
      timestamp: null
    });
  }, []);

  const setError = useCallback((errorData: ErrorState) => {
    setErrorState(errorData);
  }, []);

  const clearError = useCallback(() => {
    setErrorState({
      message: null,
      type: null,
      timestamp: null
    });
  }, []);

  return {
    error,
    showError,
    hideError,
    setError,
    clearError
  };
};

export default useErrorHandler;