/**
 * Utility functions for formatting tool calls for display
 */

import { ToolCall } from '../types/tool-call.types';

export function formatToolCallParameters(parameters: Record<string, any>): string {
  // Format parameters for display, handling sensitive data appropriately
  const formattedParams = { ...parameters };

  // Remove or mask sensitive fields
  if (formattedParams.api_key) {
    formattedParams.api_key = '***MASKED***';
  }
  if (formattedParams.token) {
    formattedParams.token = '***MASKED***';
  }

  return JSON.stringify(formattedParams, null, 2);
}

export function formatToolCallResult(result: any): string {
  // Format result for display
  if (result === null || result === undefined) {
    return 'No result';
  }

  // Handle error results specially
  if (result.error) {
    return `Error: ${result.error.message || result.error}`;
  }

  return JSON.stringify(result, null, 2);
}

export function getToolCallStatusIcon(status: ToolCall['status']): string {
  switch (status) {
    case 'success':
      return '✅';
    case 'error':
      return '❌';
    case 'pending':
      return '⏳';
    default:
      return '❓';
  }
}

export function getToolCallStatusColor(status: ToolCall['status']): string {
  switch (status) {
    case 'success':
      return 'text-green-600';
    case 'error':
      return 'text-red-600';
    case 'pending':
      return 'text-yellow-600';
    default:
      return 'text-gray-600';
  }
}

export function formatToolCallTimestamp(timestamp: Date): string {
  return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}