---
id: 3
title: chat-api-specification
stage: spec
date: 2026-01-12
surface: agent
model: Claude Sonnet 4.5
feature: chat-api
branch: 003-chat-api
user: claude
command: claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.3 – Chat API Specification (Stateless, Claude-ready)" --spec-type "api" --output "specs/api.chat.md" --template ".specify/templates/spec-template.md" --constraints " - Backend must use FastAPI - API must be fully stateless - Conversation state must be persisted in the database - API must integrate OpenAI Agents SDK - API must invoke MCP tools via the agent only - API must NOT store state in memory " --instructions " Create the FINAL canonical specification for the Chat API endpoint used by the Todo AI Chatbot. The specification MUST define the endpoint: POST /api/{user_id}/chat REQUIRED BEHAVIOR: - Accept a natural language message from the user - Optionally accept a conversation_id - Create a new conversation if conversation_id is not provided - Load full conversation history from the database - Persist the incoming user message - Invoke the OpenAI Agent with the full message history - Allow the agent to call MCP tools - Capture and persist: • Assistant response • Tool calls made by the agent - Return: • conversation_id • assistant response text • list of tool calls (if any) The specification MUST include: - Request schema (fields, types, required/optional) - Response schema - Detailed step-by-step request lifecycle - Error handling rules - Stateless execution guarantees - Multi-user isolation rules - Restart/resume behavior (server restarts must not break conversations) HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.3-chat-api-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or next steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.3-chat-api-specification.md written in very easy-to-understand technical English so the API behavior can be reviewed, debugged, and audited later. The Chat API specification must be strict, unambiguous, production-ready, and suitable for direct FastAPI implementation in later phases. " --memory-update --history-log --no-implementation
labels: [api, chat, specification, todo]
links:
  spec: specs/003-chat-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/003-chat-api/spec.md
 - specs/api.chat.md
 - history/phr/phase-1.3-chat-api-specification.md
 - history/docs/phase-1.3-chat-api-specification.md
 - history/prompts/003-chat-api/003-chat-api-specification.spec.prompt.md
tests:
 - null
---

## Prompt

claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.3 – Chat API Specification (Stateless, Claude-ready)" --spec-type "api" --output "specs/api.chat.md" --template ".specify/templates/spec-template.md" --constraints " - Backend must use FastAPI - API must be fully stateless - Conversation state must be persisted in the database - API must integrate OpenAI Agents SDK - API must invoke MCP tools via the agent only - API must NOT store state in memory " --instructions " Create the FINAL canonical specification for the Chat API endpoint used by the Todo AI Chatbot. The specification MUST define the endpoint: POST /api/{user_id}/chat REQUIRED BEHAVIOR: - Accept a natural language message from the user - Optionally accept a conversation_id - Create a new conversation if conversation_id is not provided - Load full conversation history from the database - Persist the incoming user message - Invoke the OpenAI Agent with the full message history - Allow the agent to call MCP tools - Capture and persist: • Assistant response • Tool calls made by the agent - Return: • conversation_id • assistant response text • list of tool calls (if any) The specification MUST include: - Request schema (fields, types, required/optional) - Response schema - Detailed step-by-step request lifecycle - Error handling rules - Stateless execution guarantees - Multi-user isolation rules - Restart/resume behavior (server restarts must not break conversations) HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.3-chat-api-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or next steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.3-chat-api-specification.md written in very easy-to-understand technical English so the API behavior can be reviewed, debugged, and audited later. The Chat API specification must be strict, unambiguous, production-ready, and suitable for direct FastAPI implementation in later phases. " --memory-update --history-log --no-implementation

## Response snapshot

Successfully created the Chat API Specification for the Todo AI Chatbot with the following artifacts:

1. Created feature branch `003-chat-api` with comprehensive spec document at `specs/003-chat-api/spec.md`
2. Generated the main Chat API specification file at `specs/api.chat.md` containing:
   - Complete endpoint definition for POST /api/{user_id}/chat
   - Request and response schemas with examples
   - 10-step detailed request lifecycle
   - Stateless execution guarantees
   - Multi-user isolation rules
   - Error handling procedures
   - Restart/resume behavior specifications
3. Created documentation files:
   - `history/phr/phase-1.3-chat-api-specification.md`
   - `history/docs/phase-1.3-chat-api-specification.md`
4. Created this PHR file for tracking purposes

The specification defines a stateless FastAPI endpoint that integrates with the TodoAgent through OpenAI Agents SDK, persists conversation state to the database, and ensures all MCP tool calls are made through the agent.

## Outcome

- ✅ Impact: Created complete Chat API specification for TodoAI chatbot
- 🧪 Tests: null
- 📁 Files: Created 5 files related to Chat API specification
- 🔁 Next prompts: Implement Chat API using FastAPI
- 🧠 Reflection: Specification follows all required constraints and is ready for implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of Chat API