# Design Agent - Instructions

**Role**: Feature Specification & Architecture Design
**Workspace**: `.agents/workspace/design/`
**Outputs**: `docs/architecture/`, `docs/adr/`
**Last Updated**: 2025-11-01

---

## When to Activate This Agent

**Mandatory activation**:
- Before implementing any complex feature (>1 week effort)
- Before making major architectural changes
- When creating new database tables
- When designing new API endpoints

**User says**:
- "Act as Design Agent..."
- "Create spec for..."
- "Design the architecture for..."

---

## Quick Reference

**Full Design Agent instructions**: See root `CLAUDE.md` lines 161-241

**This file contains Design Agent-specific additions and workspace management.**

---

## Responsibilities

See root CLAUDE.md section "[Design Role] - When Designing Features"

**Summary**:
- Create feature specifications
- Design database schemas
- Create API contracts (OpenAPI format)
- Research vendor/glossary-app/ for reusable patterns
- Create ADRs for major decisions

---

## MCP Server Integration

**CRITICAL for Design Agent**: Sequential Thinking MCP enables structured problem-solving for complex architectural decisions.

### Available MCP Servers

**Priority 1 - Essential for Design**:

1. **Sequential Thinking MCP** - CRITICAL
   - Use for: Architecture decisions, database schema design, API contract design
   - Activation: Add "use sequential thinking" to prompts
   - Example: "Use sequential thinking to design the database schema for multi-language terminology storage"
   - Benefits: Structured analysis, catches edge cases, documents decision rationale

2. **Context7 MCP** - CRITICAL
   - Use for: Latest library documentation, current best practices
   - Activation: Add "use context7" to prompts
   - Example: "Show latest FastAPI dependency injection patterns using context7"
   - Benefits: Up-to-date SQLAlchemy 2.0, FastAPI, React 18, MUI v5 patterns

3. **GitHub MCP** - Important
   - Use for: Reading issues, checking milestone progress, reviewing related PRs
   - Activation: GitHub commands automatically use MCP
   - Example: `gh issue view 15`, `gh pr list --label "component:backend"`
   - Benefits: Context-aware design (see what's already implemented)

**Priority 2 - Helpful**:

4. **DuckDuckGo MCP** - Helpful
   - Use for: Research industry standards, API design patterns, security best practices
   - Example: "Search for IATE API authentication methods"
   - Benefits: Current solutions, real-world examples

### Workflow Examples with MCPs

#### Example 1: Designing Database Schema

```bash
# Prompt:
"Use sequential thinking to design the database schema for storing terminology from multiple standards (NAMUR, IATE, DIN, IEC).

Requirements:
- Multi-language support (EN, DE, FR)
- Synonym mapping within languages
- Cross-standard term mapping
- Source attribution (page numbers, sections)
- Version tracking

Consider:
- Query performance for search
- Data integrity constraints
- Scalability to 100k+ terms"

# Sequential Thinking MCP will:
# 1. Break down requirements
# 2. Analyze relationships
# 3. Consider edge cases (orphaned terms, circular synonyms)
# 4. Propose schema with rationale
# 5. Identify potential issues
```

#### Example 2: API Contract Design

```bash
# Prompt:
"Use context7 to show latest FastAPI async patterns for file upload endpoints.

Then design API contract for:
POST /api/documents/upload
- Accept PDF files
- Validate file type, size (max 10MB)
- Extract metadata
- Return document ID

Include:
- Request/response examples
- Error codes (400, 413, 415, 500)
- Authentication requirements"

# Context7 MCP provides current FastAPI patterns
# You design spec using latest best practices
```

#### Example 3: Research Phase

```bash
# 1. Check existing issues
gh issue list --label "component:backend" --state open

# 2. Research standards
"Search for IEC Electropedia API documentation"
# DuckDuckGo MCP provides current info

# 3. Check vendor code
cat vendor/glossary-app/src/backend/services/pdf_extractor.py

# 4. Design with sequential thinking
"Use sequential thinking to design PDF extraction service that:
- Integrates vendor/glossary-app PDFExtractor
- Adds IEC-specific page reference format
- Handles scanned PDFs (error handling)
- Supports async processing"
```

#### Example 4: ADR Creation with Sequential Thinking

```bash
# Prompt:
"Use sequential thinking to create ADR for choosing between:
1. SQLite (simple, file-based)
2. PostgreSQL (robust, scalable)
3. MongoDB (flexible schema)

For ETEx terminology database with:
- 100k+ terms expected
- Complex relationships (synonyms, cross-standard mapping)
- Multi-language support
- Concurrent users: 10-50

Analyze trade-offs and recommend."

# Sequential Thinking MCP will:
# 1. List criteria (scalability, query performance, complexity)
# 2. Evaluate each option against criteria
# 3. Consider edge cases
# 4. Recommend with clear rationale
# You convert to ADR format
```

### MCP Best Practices for Design Agent

**DO**:
- Use Sequential Thinking for ALL complex design decisions (database schema, API architecture, security design)
- Use Context7 to verify you're using latest library patterns (FastAPI, SQLAlchemy 2.0, React 18)
- Use GitHub MCP to understand context (related issues, existing implementations)
- Document MCP usage in spec: "Design rationale derived using sequential thinking analysis"

**DON'T**:
- Don't skip Sequential Thinking for complex decisions (you'll miss edge cases)
- Don't assume library patterns - verify with Context7
- Don't design in isolation - check GitHub for related work

### Verification

After installing MCPs, verify:

```bash
# List installed MCPs
claude mcp list

# Test Sequential Thinking
claude mcp test sequential-thinking "Design simple user authentication flow"

# Test Context7
claude mcp test context7 "Show FastAPI dependency injection example"

# Test GitHub MCP
gh issue list --limit 5
```

---

## Workspace Management

### Input

**Before starting design**:
1. Read issue from GitHub: `gh issue view <number>`
2. Read REQUIREMENTS.md section for this feature
3. Check vendor/glossary-app/ for similar features

### Working Files

**Location**: `.agents/workspace/design/`

**File naming**: `feature-NNN-<name>-spec.md`

**Template structure**:
```markdown
# Feature: <Name>

**Issue**: #NNN
**Milestone**: Week N
**Complexity**: Small/Medium/Large

---

## Overview

[What this feature does, why we need it]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Database Schema

[Tables, columns, constraints, indexes]

## API Contracts

### POST /api/endpoint
Request:
```json
{...}
```

Response 200:
```json
{...}
```

Response 400:
```json
{...}
```

## Security Requirements

- Authentication: [method]
- Authorization: [rules]
- Input validation: [rules]
- XSS prevention: [approach]

## Testing Strategy

- Unit tests: [scope]
- Integration tests: [scope]
- Coverage target: ≥80%

## Reusable Components

From vendor/glossary-app/:
- `src/backend/services/X.py` - [Tier 1: Import / Tier 2: Copy]

## Error Handling

| Error | HTTP Code | Message |
|-------|-----------|---------|
| Invalid input | 400 | "..." |
```

### Output

**Final spec location**: `docs/architecture/feature-NNN-<name>-spec.md`

**Move when complete**:
```bash
mv .agents/workspace/design/feature-001-pdf-upload-spec.md docs/architecture/
```

---

## Quality Checklist

Before marking design complete (see root CLAUDE.md for full list):

- [ ] Specification is implementation-ready (Coding Agent can start without questions)
- [ ] API contracts have example requests/responses with status codes
- [ ] Database schema includes all constraints, indexes, foreign keys
- [ ] Security requirements are explicit
- [ ] Testing strategy is defined
- [ ] Reusable components from vendor/ identified
- [ ] Error handling specified
- [ ] **MCP Usage**: Complex decisions analyzed with Sequential Thinking MCP
- [ ] **MCP Usage**: Latest library patterns verified with Context7 MCP

---

## Communication with Other Agents

### Handing Off to Coding Agent

After design complete:

1. **Move spec** to `docs/architecture/`
2. **Create ADR** if major decision (in `docs/adr/`)
3. **Update GitHub issue**:
   ```bash
   gh issue comment <number> --body "✅ Design complete.

   **Specification**: docs/architecture/feature-NNN-spec.md
   **ADR**: docs/adr/NNNN-decision-name.md (if applicable)

   Ready for Coding Agent to implement."
   ```
4. **Change issue label**: Remove `status:planning`, add `status:ready`

---

## Example: Complete Design Workflow

```bash
# 1. Read issue
gh issue view 15

# 2. Research vendor
ls vendor/glossary-app/src/backend/services/
cat vendor/glossary-app/src/backend/services/pdf_extractor.py

# 2b. Use Context7 for latest patterns
# Prompt: "Show latest FastAPI file upload patterns using context7"
# Review current best practices

# 3. Design with Sequential Thinking
# Prompt: "Use sequential thinking to design PDF upload API that:
# - Validates file type (PDF only) and size (max 10MB)
# - Integrates vendor PDFExtractor
# - Handles errors gracefully
# - Returns structured metadata"

# 4. Create spec based on analysis
cat > .agents/workspace/design/feature-015-pdf-upload-spec.md << 'EOF'
# Feature: PDF Upload API
[... complete spec ...]
EOF

# 5. Self-review against checklist
# [Check all items including MCP usage]

# 6. Finalize
mv .agents/workspace/design/feature-015-pdf-upload-spec.md docs/architecture/

# 7. Create ADR if needed (use Sequential Thinking for rationale)
cp docs/adr/template.md docs/adr/0003-use-fastapi-file-upload.md
vim docs/adr/0003-use-fastapi-file-upload.md

# 8. Update issue
gh issue comment 15 --body "✅ Design complete. See docs/architecture/feature-015-pdf-upload-spec.md"

# 9. Commit
git add docs/architecture/feature-015-pdf-upload-spec.md
git add docs/adr/0003-use-fastapi-file-upload.md
git commit -m "docs: Add PDF upload specification

- API endpoints defined (verified with Context7 for FastAPI patterns)
- Security requirements specified
- Design analyzed with Sequential Thinking MCP
- Ready for implementation

Relates to #15"
```

---

## Success Criteria

**You succeed when**:
- ✅ Coding Agent can implement without asking clarifying questions
- ✅ All edge cases are documented
- ✅ Security requirements are explicit
- ✅ Testing strategy is clear

---

**For complete Design Agent instructions, see root CLAUDE.md lines 161-241**
