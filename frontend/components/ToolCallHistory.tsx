import React, { useState } from 'react';
import { ToolCall, ToolCallHistoryProps } from '../types/tool-call.types';
import { formatToolCallParameters, formatToolCallResult, getToolCallStatusIcon, getToolCallStatusColor, formatToolCallTimestamp } from '../utils/tool-call-formatter';

const ToolCallHistory: React.FC<ToolCallHistoryProps> = ({ toolCalls, onToolCallSelect }) => {
  const [expandedToolCallId, setExpandedToolCallId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedToolCallId(expandedToolCallId === id ? null : id);
  };

  // Group tool calls by date
  const groupedToolCalls = toolCalls.reduce((acc, toolCall) => {
    const date = toolCall.timestamp.toDateString();
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(toolCall);
    return acc;
  }, {} as Record<string, ToolCall[]>);

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Tool Call History</h3>

      {toolCalls.length === 0 ? (
        <p className="text-gray-500 text-center py-4">No tool calls recorded yet</p>
      ) : (
        <div className="space-y-4">
          {Object.entries(groupedToolCalls).map(([date, calls]) => (
            <div key={date}>
              <h4 className="font-medium text-gray-700 border-b pb-1">{date}</h4>
              <div className="mt-2 space-y-2">
                {calls.map((toolCall) => {
                  const isExpanded = expandedToolCallId === toolCall.id;
                  const statusColor = getToolCallStatusColor(toolCall.status);
                  const statusIcon = getToolCallStatusIcon(toolCall.status);

                  return (
                    <div
                      key={toolCall.id}
                      className={`border rounded p-3 cursor-pointer hover:bg-gray-50 transition-colors ${onToolCallSelect ? 'hover:shadow-sm' : ''}`}
                      onClick={() => onToolCallSelect && onToolCallSelect(toolCall)}
                    >
                      <div
                        className="flex justify-between items-center"
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleExpand(toolCall.id);
                        }}
                      >
                        <div className="flex items-center space-x-2">
                          <span className={statusColor}>{statusIcon}</span>
                          <span className="font-medium">{toolCall.toolName}</span>
                          <span className="text-xs text-gray-500">
                            {formatToolCallTimestamp(toolCall.timestamp)}
                          </span>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded ${statusColor.replace('text', 'bg-opacity-20 bg').replace('600', '500')}`}>
                          {toolCall.status.toUpperCase()}
                        </span>
                      </div>

                      {isExpanded && (
                        <div className="mt-3 pt-3 border-t space-y-3">
                          <div>
                            <h5 className="text-sm font-medium text-gray-700">Parameters</h5>
                            <pre className="text-xs bg-gray-100 p-2 mt-1 rounded overflow-x-auto max-w-md">
                              {formatToolCallParameters(toolCall.parameters)}
                            </pre>
                          </div>
                          <div>
                            <h5 className="text-sm font-medium text-gray-700">Result</h5>
                            <pre className="text-xs bg-gray-100 p-2 mt-1 rounded overflow-x-auto max-w-md">
                              {formatToolCallResult(toolCall.result)}
                            </pre>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ToolCallHistory;