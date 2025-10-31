# ETEx Permanent Agent System

**Purpose**: Specialized agents with dedicated roles for consistent project workflows
**Last Updated**: 2025-10-31

---

## Overview

ETEx uses **permanent agents** - specialized Claude Code instances with specific, repeating responsibilities. Each agent has its own folder with dedicated CLAUDE.md instructions.

---

## Permanent Agents

| Agent | Purpose | When to Use | Mandatory? |
|-------|---------|-------------|------------|
| **[Issue Manager](issue-manager/)** | Create/update/close GitHub issues | Any issue operation | ✅ Yes - for closing issues |
| **[Review Coordinator](review-coordinator/)** | Review docs/code/scripts for compliance | Before committing to CLAUDE.md, scripts/ | ✅ Yes - for CLAUDE.md changes |
| **[Design](design/)** | Create feature specifications | Before implementing new features | ✅ Yes - for complex features |
| **[Coding](coding/)** | Implement features per spec | Feature implementation | No - main agent can code |
| **[Testing](testing/)** | Run tests, report failures | Before PR, after implementation | ⚠️ Recommended |
| **[Backend Expert](backend-expert/)** | Python/FastAPI/SQLAlchemy best practices | Backend features, DB migrations | ✅ Yes - for backend work |
| **[Frontend Expert](frontend-expert/)** | React/TypeScript/MUI architecture | Complex UI, state management | ✅ Yes - for frontend work |
| **[Project Manager](project-manager/)** | Sprint planning, milestone tracking | Weekly reviews, sprint planning | ✅ Yes - for sprint management |

---

## Folder Structure

Each agent has:
```
.agents/<agent-name>/
├── CLAUDE.md          # Agent-specific instructions
├── workspace/         # Temporary working files (gitignored)
└── outputs/           # Final deliverables (committed)
```

---

## How to Use Permanent Agents

### Method 1: Explicit Agent Invocation

Tell Claude Code which agent to use:
```
User: "Act as Issue Manager - close issue #23 with verification"
User: "Switch to Review Coordinator - review the new script structure"
User: "As Design Agent, create spec for PDF upload feature"
```

### Method 2: Automatic Detection (via root CLAUDE.md)

Root CLAUDE.md contains triggers that automatically activate agents:
- Closing issue → Issue Manager activates
- CLAUDE.md modified → Review Coordinator activates
- "create spec" mentioned → Design Agent activates

---

## Mandatory Agent Usage

**These tasks REQUIRE specific agents**:

1. **Closing any GitHub issue** → Issue Manager
   - Ensures verification comment added
   - Ensures CHANGELOG updated if needed
   - Creates proper closure documentation

2. **Modifying CLAUDE.md** → Review Coordinator
   - Checks for contradictions
   - Ensures formatting consistency
   - Verifies rules are actionable

3. **Modifying scripts/** → Review Coordinator
   - Verifies subfolder + README structure
   - Checks script header compliance
   - Ensures category README updated

4. **Implementing complex features** → Design Agent first
   - Creates specification
   - Defines API contracts
   - Specifies testing strategy

---

## Agent Communication

**Agents communicate via**:
1. **GitHub Issues** - Issue Manager creates issues, other agents work on them
2. **Workspace files** - Agents leave files in `.agents/<agent>/workspace/` for handoff
3. **Output files** - Final deliverables in `.agents/<agent>/outputs/`

**Example workflow**:
```
Review Coordinator finds problem
  → Creates issue via Issue Manager
  → Issue Manager assigns to milestone
  → Design Agent creates spec
  → Coding Agent implements
  → Testing Agent verifies
  → Issue Manager closes with verification
```

---

## Quick Reference

**To activate an agent**:
- Read its CLAUDE.md: `.agents/<agent-name>/CLAUDE.md`
- Follow its specific workflow
- Output to its outputs/ folder

**See root CLAUDE.md** for global rules that apply to ALL agents.

---

**For detailed instructions, see each agent's CLAUDE.md file.**
