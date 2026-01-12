import React from 'react';
import { ToolCall, ToolCallDisplayProps } from '../types/tool-call.types';
import { formatToolCallParameters, formatToolCallResult, getToolCallStatusIcon, getToolCallStatusColor, formatToolCallTimestamp } from '../utils/tool-call-formatter';

const ToolCallDisplay: React.FC<ToolCallDisplayProps> = ({ toolCall }) => {
  const statusColor = getToolCallStatusColor(toolCall.status);
  const statusIcon = getToolCallStatusIcon(toolCall.status);

  return (
    <div className="border-l-4 border-blue-500 pl-4 py-2 my-2 bg-gray-50 rounded-r">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className={`font-bold ${statusColor}`}>
            {statusIcon} {toolCall.toolName}
          </span>
          <span className="text-xs text-gray-500">
            {formatToolCallTimestamp(toolCall.timestamp)}
          </span>
        </div>
        <span className={`text-xs px-2 py-1 rounded ${statusColor.replace('text', 'bg-opacity-20 bg').replace('600', '500')}`}>
          {toolCall.status.toUpperCase()}
        </span>
      </div>

      <details className="mt-2">
        <summary className="cursor-pointer text-sm text-gray-700 hover:text-gray-900">
          Parameters
        </summary>
        <pre className="text-xs bg-white p-2 mt-1 rounded border overflow-x-auto max-w-md">
          {formatToolCallParameters(toolCall.parameters)}
        </pre>
      </details>

      <details className="mt-2">
        <summary className="cursor-pointer text-sm text-gray-700 hover:text-gray-900">
          Result
        </summary>
        <pre className="text-xs bg-white p-2 mt-1 rounded border overflow-x-auto max-w-md">
          {formatToolCallResult(toolCall.result)}
        </pre>
      </details>
    </div>
  );
};

interface ToolCallVisualizerProps {
  toolCalls: ToolCall[];
  isVisible?: boolean;
}

const ToolCallVisualizer: React.FC<ToolCallVisualizerProps> = ({ toolCalls, isVisible = true }) => {
  if (!isVisible || !toolCalls.length) {
    return null;
  }

  return (
    <div className="mt-4 border-t pt-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-2">Tool Calls</h3>
      <div className="space-y-2">
        {toolCalls.map((toolCall) => (
          <ToolCallDisplay key={toolCall.id} toolCall={toolCall} />
        ))}
      </div>
    </div>
  );
};

export default ToolCallVisualizer;