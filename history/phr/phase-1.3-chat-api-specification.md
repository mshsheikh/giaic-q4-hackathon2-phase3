# PHR: Phase 1.3 - Chat API Specification

**Date**: 2026-01-12
**Phase**: Hackathon 2 – Phase 3
**Step**: PHASE 1.3 – Chat API Specification (Stateless, Claude-ready)
**Command**: `claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.3 – Chat API Specification (Stateless, Claude-ready)" --spec-type "api" --output "specs/api.chat.md" --template ".specify/templates/spec-template.md" --constraints " - Backend must use FastAPI - API must be fully stateless - Conversation state must be persisted in the database - API must integrate OpenAI Agents SDK - API must invoke MCP tools via the agent only - API must NOT store state in memory " --instructions " Create the FINAL canonical specification for the Chat API endpoint used by the Todo AI Chatbot. The specification MUST define the endpoint: POST /api/{user_id}/chat REQUIRED BEHAVIOR: - Accept a natural language message from the user - Optionally accept a conversation_id - Create a new conversation if conversation_id is not provided - Load full conversation history from the database - Persist the incoming user message - Invoke the OpenAI Agent with the full message history - Allow the agent to call MCP tools - Capture and persist: • Assistant response • Tool calls made by the agent - Return: • conversation_id • assistant response text • list of tool calls (if any) The specification MUST include: - Request schema (fields, types, required/optional) - Response schema - Detailed step-by-step request lifecycle - Error handling rules - Stateless execution guarantees - Multi-user isolation rules - Restart/resume behavior (server restarts must not break conversations) HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.3-chat-api-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or next steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.3-chat-api-specification.md written in very easy-to-understand technical English so the API behavior can be reviewed, debugged, and audited later. The Chat API specification must be strict, unambiguous, production-ready, and suitable for direct FastAPI implementation in later phases. " --memory-update --history-log --no-implementation`
**Files Modified**:
 - specs/003-chat-api/spec.md
 - specs/api.chat.md
 - history/phr/phase-1.3-chat-api-specification.md
 - history/docs/phase-1.3-chat-api-specification.md

## Summary

Successfully created the final canonical Chat API Specification for the Todo AI Chatbot. The specification defines the POST /api/{user_id}/chat endpoint with complete request/response schemas, detailed request lifecycle, stateless execution guarantees, and multi-user isolation rules.

## What Was Done

1. Created feature branch `003-chat-api` with comprehensive spec document
2. Generated detailed Chat API specification document (specs/api.chat.md) containing:
   - Complete endpoint definition for POST /api/{user_id}/chat
   - Request and response schemas with examples
   - 10-step detailed request lifecycle
   - Stateless execution guarantees
   - Multi-user isolation rules
   - Error handling procedures
   - Restart/resume behavior specifications
3. Created documentation files as required by the specification

## Known Limitations

- The API relies on the availability of the OpenAI Agents SDK
- MCP tools must be implemented separately before the API can be fully functional
- Database schema definitions are implied but not explicitly detailed in this specification

## Next Steps

- Implement the Chat API using FastAPI based on this specification
- Design the underlying database schema to support conversation and message persistence
- Integrate with the TodoAgent and MCP tools
- Test the API with various conversation scenarios