---
id: 2
title: mcp-tool-specification
stage: spec
date: 2026-01-12
surface: agent
model: Claude Sonnet 4.5
feature: mcp-tools
branch: 002-mcp-tools
user: claude
command: claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.2 – MCP Tool Specification (Final, Claude-ready)" --spec-type "mcp-tools" --output "specs/mcp.tools.md" --template ".specify/templates/spec-template.md" --constraints " - Use Official MCP SDK only - MCP tools must be fully stateless - MCP tools must NOT store in-memory state - MCP tools must persist all state to the database - MCP tools must be callable independently and via agent - MCP tools must enforce strict input/output schemas " --instructions " Create the FINAL canonical MCP Tool Specification for the Todo AI Chatbot. The specification MUST define the following tools exactly: 1. add_task 2. list_tasks 3. complete_task 4. delete_task 5. update_task For EACH tool, clearly specify: - Purpose - Exact input parameters (types, required/optional) - Output schema - Example input - Example output - Error cases (task not found, invalid input, permission issues) - Stateless execution rules - Database interaction responsibility - Idempotency considerations (where applicable) GLOBAL MCP RULES: - Tools must never assume prior calls - Tools must never depend on agent memory - All user scoping must be enforced via user_id - Tools must return structured, predictable responses - Errors must be machine-readable and human-safe HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.2-mcp-tool-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or follow-up steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.2-mcp-tool-specification.md written in very easy-to-understand technical English so the MCP behavior can be reviewed, debugged, and audited later. The MCP Tool Specification must be strict, unambiguous, production-ready, and suitable for direct implementation using the Official MCP SDK in later phases. " --memory-update --history-log --no-implementation
labels: [mcp, tools, specification, todo]
links:
  spec: specs/002-mcp-tools/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-mcp-tools/spec.md
 - specs/mcp.tools.md
 - history/phr/phase-1.2-mcp-tool-specification.md
 - history/docs/phase-1.2-mcp-tool-specification.md
 - history/prompts/002-mcp-tools/002-mcp-tool-specification.spec.prompt.md
tests:
 - null
---

## Prompt

claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.2 – MCP Tool Specification (Final, Claude-ready)" --spec-type "mcp-tools" --output "specs/mcp.tools.md" --template ".specify/templates/spec-template.md" --constraints " - Use Official MCP SDK only - MCP tools must be fully stateless - MCP tools must NOT store in-memory state - MCP tools must persist all state to the database - MCP tools must be callable independently and via agent - MCP tools must enforce strict input/output schemas " --instructions " Create the FINAL canonical MCP Tool Specification for the Todo AI Chatbot. The specification MUST define the following tools exactly: 1. add_task 2. list_tasks 3. complete_task 4. delete_task 5. update_task For EACH tool, clearly specify: - Purpose - Exact input parameters (types, required/optional) - Output schema - Example input - Example output - Error cases (task not found, invalid input, permission issues) - Stateless execution rules - Database interaction responsibility - Idempotency considerations (where applicable) GLOBAL MCP RULES: - Tools must never assume prior calls - Tools must never depend on agent memory - All user scoping must be enforced via user_id - Tools must return structured, predictable responses - Errors must be machine-readable and human-safe HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.2-mcp-tool-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or follow-up steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.2-mcp-tool-specification.md written in very easy-to-understand technical English so the MCP behavior can be reviewed, debugged, and audited later. The MCP Tool Specification must be strict, unambiguous, production-ready, and suitable for direct implementation using the Official MCP SDK in later phases. " --memory-update --history-log --no-implementation

## Response snapshot

Successfully created the MCP Tool Specification for the Todo AI Chatbot with the following artifacts:

1. Created feature branch `002-mcp-tools` with comprehensive spec document at `specs/002-mcp-tools/spec.md`
2. Generated the main MCP tools specification file at `specs/mcp.tools.md` containing detailed definitions of all 5 required tools:
   - add_task: Creates new tasks with proper validation and error handling
   - list_tasks: Retrieves user tasks with filtering and pagination support
   - complete_task: Updates task status to completed with ownership verification
   - delete_task: Removes tasks from database with authorization checks
   - update_task: Modifies task properties with partial update support
3. Created documentation files:
   - `history/phr/phase-1.2-mcp-tool-specification.md`
   - `history/docs/phase-1.2-mcp-tool-specification.md`
4. Created this PHR file for tracking purposes

The specification enforces stateless operation, strict input/output schemas, user isolation via user_id, and proper error handling for all tools.

## Outcome

- ✅ Impact: Created complete MCP tool specification for TodoAI chatbot
- 🧪 Tests: null
- 📁 Files: Created 5 files related to MCP tool specification
- 🔁 Next prompts: Implement MCP tools using Official MCP SDK
- 🧠 Reflection: Specification follows all required constraints and is ready for implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of MCP tools