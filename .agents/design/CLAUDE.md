# Design Agent - Instructions

**Role**: Feature Specification & Architecture Design
**Workspace**: `.agents/workspace/design/`
**Outputs**: `docs/architecture/`, `docs/adr/`
**Last Updated**: 2025-10-31

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

# 3. Create spec
cat > .agents/workspace/design/feature-015-pdf-upload-spec.md << 'EOF'
# Feature: PDF Upload API
[... complete spec ...]
EOF

# 4. Self-review against checklist
# [Check all items]

# 5. Finalize
mv .agents/workspace/design/feature-015-pdf-upload-spec.md docs/architecture/

# 6. Create ADR if needed
cp docs/adr/template.md docs/adr/0003-use-fastapi-file-upload.md
vim docs/adr/0003-use-fastapi-file-upload.md

# 7. Update issue
gh issue comment 15 --body "✅ Design complete. See docs/architecture/feature-015-pdf-upload-spec.md"

# 8. Commit
git add docs/architecture/feature-015-pdf-upload-spec.md
git add docs/adr/0003-use-fastapi-file-upload.md
git commit -m "docs: Add PDF upload specification

- API endpoints defined
- Security requirements specified
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
