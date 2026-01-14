# PHR: Phase 1.2 - MCP Tool Specification

**Date**: 2026-01-12
**Phase**: Hackathon 2 – Phase 3
**Step**: PHASE 1.2 – MCP Tool Specification (Final, Claude-ready)
**Command**: `claude code sp.specify --phase "Hackathon 2 – Phase 3" --step "PHASE 1.2 – MCP Tool Specification (Final, Claude-ready)" --spec-type "mcp-tools" --output "specs/mcp.tools.md" --template ".specify/templates/spec-template.md" --constraints " - Use Official MCP SDK only - MCP tools must be fully stateless - MCP tools must NOT store in-memory state - MCP tools must persist all state to the database - MCP tools must be callable independently and via agent - MCP tools must enforce strict input/output schemas " --instructions " Create the FINAL canonical MCP Tool Specification for the Todo AI Chatbot. The specification MUST define the following tools exactly: 1. add_task 2. list_tasks 3. complete_task 4. delete_task 5. update_task For EACH tool, clearly specify: - Purpose - Exact input parameters (types, required/optional) - Output schema - Example input - Example output - Error cases (task not found, invalid input, permission issues) - Stateless execution rules - Database interaction responsibility - Idempotency considerations (where applicable) GLOBAL MCP RULES: - Tools must never assume prior calls - Tools must never depend on agent memory - All user scoping must be enforced via user_id - Tools must return structured, predictable responses - Errors must be machine-readable and human-safe HISTORY & DOCUMENTATION REQUIREMENTS (MANDATORY): 1. Log this command execution under: /history/phr/phase-1.2-mcp-tool-specification.md 2. The history log MUST include: - Timestamp - Phase and step name - Exact Claude Code command executed - Files created or modified - Clear summary of what was done - Known limitations or follow-up steps 3. Maintain a human-readable technical explanation of this phase in: /history/docs/phase-1.2-mcp-tool-specification.md written in very easy-to-understand technical English so the MCP behavior can be reviewed, debugged, and audited later. The MCP Tool Specification must be strict, unambiguous, production-ready, and suitable for direct implementation using the Official MCP SDK in later phases. " --memory-update --history-log --no-implementation`
**Files Modified**:
 - specs/002-mcp-tools/spec.md
 - specs/mcp.tools.md
 - history/phr/phase-1.2-mcp-tool-specification.md
 - history/docs/phase-1.2-mcp-tool-specification.md

## Summary

Successfully created the final canonical MCP Tool Specification for the Todo AI Chatbot. The specification defines five essential tools: add_task, list_tasks, complete_task, delete_task, and update_task, each with precise input/output schemas, error handling, and stateless execution rules.

## What Was Done

1. Created feature branch `002-mcp-tools` with comprehensive spec document
2. Generated detailed MCP tool specification document (specs/mcp.tools.md) containing:
   - Complete definitions for all 5 required tools
   - Input/output schemas with examples
   - Error cases and handling procedures
   - Stateless execution rules
   - Database interaction responsibilities
   - Idempotency considerations
3. Created documentation files as required by the specification

## Known Limitations

- The tools are designed to be stateless and rely entirely on database persistence
- User authentication mechanisms are assumed but not specified in detail
- Database schema definitions are implied but not explicitly detailed in this specification

## Next Steps

- Implement the MCP tools using the Official MCP SDK based on this specification
- Design the underlying database schema to support the required operations
- Integrate the tools with the TodoAgent for natural language processing
- Test the tools independently and through the agent interface