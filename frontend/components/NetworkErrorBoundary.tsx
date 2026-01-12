import React from 'react';

interface NetworkErrorBoundaryProps {
  children: React.ReactNode;
  onRetry?: () => void;
  retryLabel?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class NetworkErrorBoundary extends React.Component<NetworkErrorBoundaryProps, State> {
  constructor(props: NetworkErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    // Check if the error is related to network issues
    if (
      error.message.includes('Failed to fetch') ||
      error.message.includes('Network Error') ||
      error.message.includes('TypeError: fetch') ||
      error.name === 'TypeError' // Often indicates network issues
    ) {
      return { hasError: true, error };
    }

    // If it's not a network error, don't handle it here
    return { hasError: false, error: null };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('NetworkErrorBoundary caught an error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    if (this.props.onRetry) {
      this.props.onRetry();
    } else {
      window.location.reload();
    }
  };

  render() {
    if (this.state.hasError && this.state.error) {
      return (
        <div className="flex flex-col items-center justify-center p-8 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h2 className="text-xl font-bold text-yellow-700 mb-2">Network Issue</h2>
          <p className="text-yellow-600 mb-4">
            We're having trouble connecting to the server. Please check your internet connection and try again.
          </p>
          <button
            className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
            onClick={this.handleRetry}
          >
            {this.props.retryLabel || 'Try Again'}
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default NetworkErrorBoundary;