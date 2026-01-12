/**
 * Type definitions for tool call visualization
 */

export interface ToolCall {
  id: string;
  toolName: string;
  parameters: Record<string, any>;
  result: any;
  status: 'pending' | 'success' | 'error';
  timestamp: Date;
}

export interface ToolCallDisplayProps {
  toolCall: ToolCall;
}

export interface ToolCallHistoryProps {
  toolCalls: ToolCall[];
  onToolCallSelect?: (toolCall: ToolCall) => void;
}