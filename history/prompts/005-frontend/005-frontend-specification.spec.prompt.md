---
id: 5
title: frontend-specification
stage: spec
date: 2026-01-12
surface: agent
model: Claude Sonnet 4.5
feature: frontend
branch: 005-frontend
user: claude
command: claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.5 – Frontend Specification (ChatKit)" --spec-type "frontend" --output "specs/frontend.chatkit.md" --template ".specify/templates/spec-template.md" --constraints " - Frontend must use OpenAI ChatKit - Frontend must be stateless - Frontend must communicate ONLY via Chat API - Authentication must integrate with Better Auth - No business logic in frontend " --instructions " Create the FINAL canonical Frontend Specification for the Todo AI Chatbot using OpenAI ChatKit. The specification MUST include: 1. ChatKit Configuration - ChatKit initialization - Domain allowlist requirements - Domain key usage - Environment variables - Local vs production behavior 2. Authentication Handling - Integration with Better Auth - User identity propagation to backend - Session handling rules - Logout and session expiry behavior 3. Message Handling - Sending user messages to POST /api/{user_id}/chat - Handling conversation_id - Rendering assistant responses 4. Streaming vs Non-Streaming - Whether streaming is enabled or disabled - Rationale for the choice - UI behavior during agent processing 5. Tool Call Visualization - How MCP tool calls are represented in UI - Visibility rules (what the user sees vs what is hidden) - Friendly explanations for actions taken 6. Error UI - Network errors - Backend errors - Tool execution failures - Authentication errors - Empty or invalid responses 7. UX Constraints - Loading states - Disabled input during agent execution - Accessibility considerations HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.5-frontend-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or next steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.5-frontend-specification.md written in very easy-to-understand technical English so frontend behavior can be reviewed, debugged, and audited later. The frontend specification must be strict, unambiguous, production-ready, and suitable for direct ChatKit implementation in later phases. " --memory-update --history-log --no-implementation
labels: [frontend, chatkit, auth, todo]
links:
  spec: specs/005-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-frontend/spec.md
 - specs/frontend.chatkit.md
 - history/phr/phase-1.5-frontend-specification.md
 - history/docs/phase-1.5-frontend-specification.md
 - history/prompts/005-frontend/005-frontend-specification.spec.prompt.md
tests:
 - null
---

## Prompt

claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.5 – Frontend Specification (ChatKit)" --spec-type "frontend" --output "specs/frontend.chatkit.md" --template ".specify/templates/spec-template.md" --constraints " - Frontend must use OpenAI ChatKit - Frontend must be stateless - Frontend must communicate ONLY via Chat API - Authentication must integrate with Better Auth - No business logic in frontend " --instructions " Create the FINAL canonical Frontend Specification for the Todo AI Chatbot using OpenAI ChatKit. The specification MUST include: 1. ChatKit Configuration - ChatKit initialization - Domain allowlist requirements - Domain key usage - Environment variables - Local vs production behavior 2. Authentication Handling - Integration with Better Auth - User identity propagation to backend - Session handling rules - Logout and session expiry behavior 3. Message Handling - Sending user messages to POST /api/{user_id}/chat - Handling conversation_id - Rendering assistant responses 4. Streaming vs Non-Streaming - Whether streaming is enabled or disabled - Rationale for the choice - UI behavior during agent processing 5. Tool Call Visualization - How MCP tool calls are represented in UI - Visibility rules (what the user sees vs what is hidden) - Friendly explanations for actions taken 6. Error UI - Network errors - Backend errors - Tool execution failures - Authentication errors - Empty or invalid responses 7. UX Constraints - Loading states - Disabled input during agent execution - Accessibility considerations HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.5-frontend-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or next steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.5-frontend-specification.md written in very easy-to-understand technical English so frontend behavior can be reviewed, debugged, and audited later. The frontend specification must be strict, unambiguous, production-ready, and suitable for direct ChatKit implementation in later phases. " --memory-update --history-log --no-implementation

## Response snapshot

Successfully created the Frontend Specification for the Todo AI Chatbot with the following artifacts:

1. Created feature branch `005-frontend` with comprehensive spec document at `specs/005-frontend/spec.md`
2. Generated the main Frontend specification file at `specs/frontend.chatkit.md` containing:
   - Complete ChatKit configuration and initialization
   - Domain allowlist requirements and key usage
   - Environment variable management
   - Authentication integration with Better Auth
   - User identity propagation to backend
   - Session handling and logout behavior
   - Message handling and conversation_id management
   - Non-streaming implementation with rationale
   - Tool call visualization with UI examples
   - Comprehensive error handling for all error types
   - UX constraints including loading states and accessibility
   - Security and performance considerations
3. Created documentation files:
   - `history/phr/phase-1.5-frontend-specification.md`
   - `history/docs/phase-1.5-frontend-specification.md`
4. Created this PHR file for tracking purposes

The specification defines a ChatKit-based frontend that integrates with Better Auth and communicates exclusively with the backend via the Chat API.

## Outcome

- ✅ Impact: Created complete Frontend specification for TodoAI chatbot
- 🧪 Tests: null
- 📁 Files: Created 5 files related to Frontend specification
- 🔁 Next prompts: Implement frontend using OpenAI ChatKit
- 🧠 Reflection: Specification follows all required constraints and is ready for implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of frontend