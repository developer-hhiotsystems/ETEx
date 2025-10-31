# ETEx GitHub Workflow Guide

**Purpose**: Conventions for using GitHub Issues, Projects, Actions, and Wiki for ETEx development
**Last Updated**: 2025-10-31
**Version**: 1.0

---

## Table of Contents

1. [Overview](#overview)
2. [GitHub Issues - Conventions](#github-issues---conventions)
3. [GitHub Projects - Board Setup](#github-projects---board-setup)
4. [GitHub Actions - Automation](#github-actions---automation)
5. [GitHub Wiki - Documentation Strategy](#github-wiki---documentation-strategy)
6. [Pull Request Workflow](#pull-request-workflow)
7. [Simulation Examples](#simulation-examples)

---

## Overview

### What Goes Where?

| Content Type | Storage Location | Why? |
|-------------|------------------|------|
| **Requirements, Architecture** | `docs/` in repo (committed) | Version controlled, lives with code |
| **User guides, API docs** | GitHub Wiki | Easy to edit, searchable, public-facing |
| **Tasks, bugs, features** | GitHub Issues | Trackable, discussable, linkable |
| **Roadmap, sprints** | GitHub Projects | Visual progress, drag-drop, timeline |
| **CI/CD, testing, releases** | GitHub Actions | Automated quality checks |
| **Code changes** | Pull Requests | Review, discuss, merge with safety |

### Key Principle

**Single Source of Truth**:
- `docs/REQUIREMENTS.md` in repo = **authoritative spec** (rarely changes)
- GitHub Issues = **actionable tasks** derived from requirements
- GitHub Projects = **visual tracker** of issue progress
- GitHub Wiki = **public-facing documentation** (how to use ETEx)

---

## GitHub Issues - Conventions

### Issue Types (via Labels)

| Label | Color | Purpose | Example Title |
|-------|-------|---------|---------------|
| `type: feature` | `#0E8A16` (green) | New functionality | `feat: Add IATE API integration (Week 4)` |
| `type: bug` | `#D73A4A` (red) | Something broken | `bug: PDF extraction fails on scanned documents` |
| `type: docs` | `#0075CA` (blue) | Documentation only | `docs: Add API endpoint examples to Wiki` |
| `type: refactor` | `#FFA500` (orange) | Code improvement | `refactor: Extract common validation logic` |
| `type: test` | `#FBCA04` (yellow) | Testing improvements | `test: Add integration tests for search API` |
| `type: chore` | `#CCCCCC` (gray) | Maintenance tasks | `chore: Update dependencies to latest versions` |

### Priority Labels

| Label | Color | Meaning | SLA |
|-------|-------|---------|-----|
| `priority: critical` | `#B60205` (dark red) | Blocks MVP, security issue | Fix ASAP (same day) |
| `priority: high` | `#D93F0B` (red-orange) | Important for current week | Fix this week |
| `priority: medium` | `#FBCA04` (yellow) | Normal priority | Fix this sprint |
| `priority: low` | `#0E8A16` (green) | Nice to have | Post-MVP or next sprint |

### Phase Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `phase: mvp` | `#5319E7` (purple) | Must have for MVP (6 weeks) |
| `phase: 2a` | `#C5DEF5` (light blue) | Phase 2A (Internal docs) |
| `phase: 2b` | `#C5DEF5` (light blue) | Phase 2B (Deviation checking) |
| `phase: future` | `#E4E669` (pale yellow) | Ideas for later |

### Component Labels

| Label | Color | Component |
|-------|-------|-----------|
| `component: backend` | `#1D76DB` (blue) | Python/FastAPI |
| `component: frontend` | `#BFD4F2` (light blue) | React/TypeScript |
| `component: database` | `#006B75` (teal) | SQLite/Alembic |
| `component: extraction` | `#7057FF` (violet) | PDF/term extraction |
| `component: api-integration` | `#008672` (green-teal) | IATE/IEC integration |

### Status Labels (Auto-managed by Projects)

| Label | Meaning |
|-------|---------|
| `status: planning` | Spec/design in progress |
| `status: ready` | Ready for coding |
| `status: in-progress` | Currently being worked on |
| `status: review` | Code review needed |
| `status: blocked` | Waiting on external dependency |

---

## Issue Title Conventions

### Format

```
<type>(<component>): <brief description> [<week>]
```

### Examples

**Good**:
```
feat(backend): Implement PDF upload endpoint (Week 2)
bug(extraction): PDF parser fails on multi-column layouts
docs(wiki): Add IATE integration setup guide
test(api): Add integration tests for term CRUD endpoints
refactor(frontend): Extract search filters into reusable component
```

**Bad**:
```
Add feature          ❌ (too vague, no type/component)
Fix bug in code      ❌ (no component, not descriptive)
Week 2 stuff         ❌ (not actionable)
```

---

## Issue Description Template

### For Features

```markdown
## Feature Overview
Brief description of what this feature does and why it's needed.

## Acceptance Criteria
- [ ] User can upload PDF via drag-drop or file picker
- [ ] System validates file type (only .pdf accepted)
- [ ] Upload progress shown with percentage
- [ ] Success/error message displayed

## Related Spec
Link to `docs/architecture/feature-XXX-spec.md` (if exists)

## Implementation Notes
- Reuse `pdf_extractor.py` from Glossary APP (Tier 1)
- Max file size: 50MB
- Store in `data/uploads/` with timestamp prefix

## Week / Phase
Week 2 / MVP Phase 1

## Dependencies
- Depends on #5 (database schema)
- Blocks #12 (term extraction)

## Estimated Effort
🔹 Small (< 4 hours)
🔸 Medium (4-8 hours)
🔶 Large (1-2 days)
🔺 Extra Large (> 2 days)
```

### For Bugs

```markdown
## Bug Description
PDF extraction fails when processing scanned NAMUR documents with multi-column layouts.

## Steps to Reproduce
1. Upload `NAMUR-NE107-scanned.pdf`
2. Click "Extract Terms"
3. Observe error: "IndexError: list index out of range"

## Expected Behavior
Should extract terms from both columns, or gracefully handle unsupported format.

## Actual Behavior
Crashes with stack trace (see below).

## Error Log
```
[paste error log here]
```

## Environment
- Python 3.12.0
- Windows 11
- pdf_extractor.py v1.2.3

## Impact
🔴 Critical - Blocks Week 2 milestone
🟠 High - Affects core functionality
🟡 Medium - Workaround available
🟢 Low - Edge case, rare occurrence

## Proposed Fix
Add column detection logic or fallback to OCR for scanned PDFs.
```

### For Documentation

```markdown
## What Needs Documentation
API endpoint `/api/sources` - CRUD operations for authoritative sources

## Target Audience
- Frontend developers integrating with API
- External API consumers (future)

## Location
GitHub Wiki > API Reference > Authoritative Sources

## Content Needed
- Endpoint URLs
- Request/response examples (JSON)
- Status codes (200, 400, 404, 500)
- Authentication requirements (if applicable)

## Related Code
`src/backend/api/sources.py:15-87`
```

---

## GitHub Projects - Board Setup

### Recommended: Single Project Board for MVP

**Name**: "ETEx MVP - 6 Week Sprint"

### Board Views

#### 1. **Kanban View** (Default)

Columns:
```
📋 Backlog → 📐 Design → 🚀 Ready → 👨‍💻 In Progress → 👀 Review → ✅ Done
```

**Column Automation**:
- Issue opened → **Backlog**
- Label `status: ready` added → **Ready**
- Assignee added → **In Progress**
- PR opened → **Review**
- Issue closed → **Done**

#### 2. **Timeline View** (Roadmap)

- Group by: Week (Week 1, Week 2, ..., Week 6)
- Show: Start date, Due date
- Milestones: Week 1 milestone (end of week)

#### 3. **Table View** (Spreadsheet)

Columns to show:
- Title
- Type (feature/bug/docs)
- Priority
- Component
- Assignee
- Week
- Status
- Estimated effort

---

### Custom Fields for Project Board

| Field Name | Type | Values | Purpose |
|------------|------|--------|---------|
| **Week** | Single select | Week 1, Week 2, ..., Week 6, Post-MVP | Track sprint |
| **Effort** | Single select | 🔹 Small, 🔸 Medium, 🔶 Large, 🔺 XL | Size estimation |
| **Component** | Single select | Backend, Frontend, Database, Docs | Quick filter |
| **Reviewed By** | Text | Agent name or "Self" | Track reviews |

---

## GitHub Actions - Automation

### Recommended Actions (Start Simple, Expand Later)

#### 1. **Issue Labeler** (Auto-label based on title)

```yaml
# .github/workflows/issue-labeler.yml
name: Issue Labeler

on:
  issues:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Label based on title
        uses: actions/labeler@v4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/issue-labeler.yml
```

**Config** (`.github/issue-labeler.yml`):
```yaml
'type: feature':
  - 'feat*'
  - 'feature*'

'type: bug':
  - 'bug*'
  - 'fix*'

'type: docs':
  - 'docs*'

'component: backend':
  - '*backend*'
  - '*api*'
  - '*fastapi*'

'component: frontend':
  - '*frontend*'
  - '*react*'
  - '*ui*'
```

#### 2. **Welcome New Issues** (Friendly automation)

```yaml
# .github/workflows/welcome.yml
name: Welcome

on:
  issues:
    types: [opened]

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - name: Comment on new issue
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '👋 Thanks for opening this issue! It will be reviewed and labeled shortly.'
            })
```

#### 3. **Stale Issue Manager** (Clean up old issues)

```yaml
# .github/workflows/stale.yml
name: Close Stale Issues

on:
  schedule:
    - cron: '0 0 * * 0'  # Run weekly on Sunday

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v8
        with:
          days-before-stale: 60
          days-before-close: 7
          stale-issue-label: 'stale'
          stale-issue-message: 'This issue has been inactive for 60 days. If still relevant, please comment.'
          close-issue-message: 'Closing due to inactivity.'
```

#### 4. **Documentation Sync** (Update Wiki on docs/ changes)

**Future**: Auto-sync `docs/` changes to GitHub Wiki (Week 3+)

---

## GitHub Wiki - Documentation Strategy

### What Goes in Wiki vs Repo?

| Content | Repo (`docs/`) | Wiki | Why? |
|---------|----------------|------|------|
| **Requirements** | ✅ `docs/REQUIREMENTS.md` | ❌ | Version controlled, changes tracked |
| **ADRs** | ✅ `docs/adr/` | ❌ | Immutable, part of codebase history |
| **Setup Guide** | ✅ `docs/getting-started/SETUP.md` | ✅ (mirror) | Repo = authoritative, Wiki = discoverable |
| **API Reference** | ❌ (auto-generated) | ✅ | Easy to browse, examples, frequently updated |
| **User Guide** | ❌ | ✅ | Non-technical users, how to use ETEx |
| **FAQ** | ❌ | ✅ | Community-driven, evolves based on questions |
| **Architecture Diagrams** | ✅ `docs/architecture/` (source) | ✅ (rendered) | Repo = source control, Wiki = visual display |

### Wiki Structure (Proposed)

```
Home
├── Getting Started
│   ├── Installation (mirror of SETUP.md)
│   ├── Quick Start Guide
│   └── Troubleshooting
│
├── User Guide
│   ├── Uploading Documents
│   ├── Searching Terms
│   ├── Managing Sources
│   └── Understanding Terminology Tiers
│
├── API Reference
│   ├── Authentication (if applicable)
│   ├── Authoritative Sources API
│   ├── Documents API
│   ├── Terms API
│   ├── Translations API
│   └── Error Codes
│
├── Developer Guide
│   ├── Architecture Overview
│   ├── Database Schema
│   ├── Code Reuse from Glossary APP
│   ├── Testing Strategy
│   └── Contributing Guidelines
│
└── FAQ
    ├── General Questions
    ├── Technical Questions
    └── Roadmap & Future Features
```

### Wiki Update Workflow

**Option 1: Manual Updates** (Start with this)
- Update `docs/` in repo first (source of truth)
- Copy relevant sections to Wiki
- Add Wiki-specific enhancements (screenshots, examples)

**Option 2: Automated Sync** (Future)
- GitHub Action triggered on `docs/` changes
- Auto-sync to Wiki
- Preserve Wiki-specific formatting

---

## Pull Request Workflow

### When to Use PRs?

| Scenario | Use PR? | Why? |
|----------|---------|------|
| **Solo development** | Optional | Direct commits OK for MVP, but PR = better documentation |
| **Multi-agent work** | ✅ Yes | Review agent approves via PR |
| **Major features** | ✅ Yes | Document changes, link to issues |
| **Bug fixes** | Optional | Small fixes = direct commit; complex = PR |
| **Documentation updates** | Optional | Direct commit OK unless major restructure |

### PR Title Convention

Same as issue titles:
```
<type>(<component>): <brief description>
```

Examples:
```
feat(backend): Add PDF upload endpoint (Closes #15)
fix(extraction): Handle multi-column PDF layouts (Fixes #23)
docs(wiki): Add API reference examples
```

### PR Description Template

```markdown
## Summary
Brief description of changes (1-2 sentences).

## Changes Made
- Implemented PDF upload endpoint (`/api/documents/upload`)
- Added file type validation (only .pdf allowed)
- Integrated `pdf_extractor.py` from Glossary APP (Tier 1)
- Added unit tests with 85% coverage

## Related Issues
Closes #15
Related to #12 (term extraction)

## Testing
- [ ] Unit tests pass (`pytest tests/unit/`)
- [ ] Integration tests pass (`pytest tests/integration/`)
- [ ] Manual testing completed (uploaded 3 test PDFs)
- [ ] Coverage ≥ 80% (`pytest --cov`)

## Review Checklist
- [ ] Code follows PEP 8 / style guide
- [ ] Attribution headers on copied code (Tier 2)
- [ ] No hardcoded secrets or credentials
- [ ] Error handling implemented
- [ ] Documentation updated (if applicable)

## Screenshots (if applicable)
[Upload UI screenshot here]
```

### PR Review Process

**For Single Developer (Self-Review)**:
1. Create PR (even if solo)
2. Review your own code in GitHub UI (catches mistakes!)
3. Run full test suite
4. Merge when satisfied

**For Multi-Agent Development**:
1. Coding agent creates PR
2. Review agent assigned automatically
3. Review agent comments or approves
4. Coding agent addresses feedback
5. Review agent merges when approved

---

## Simulation Examples

Let me create realistic examples for Week 1-6:

---

### Example 1: Week 1 Feature Issue

**Title**: `feat(backend): Create database schema with SQLAlchemy models (Week 1)`

**Labels**: `type: feature`, `priority: high`, `phase: mvp`, `component: database`

**Description**:
```markdown
## Feature Overview
Implement the 5 core database tables using SQLAlchemy ORM as defined in docs/REQUIREMENTS.md section 13.

## Acceptance Criteria
- [ ] `authoritative_sources` table with all fields (id, name, display_name, source_type, tier, is_active, config_json, timestamps)
- [ ] `terms` table with full-text search index on `term` and `definition` fields
- [ ] `term_synonyms` table with bidirectional relationship
- [ ] `translations` table with source/target language validation
- [ ] `uploaded_documents` table with file path tracking
- [ ] All foreign keys defined with proper cascade behavior
- [ ] Indexes added for performance (source_id, language_code, etc.)
- [ ] Timestamps (created_at, updated_at) auto-managed

## Related Spec
- `docs/REQUIREMENTS.md` section 13 (Database Schema)

## Implementation Notes
- Reference `vendor/glossary-app/src/backend/models/base_models.py` for pattern (Tier 3)
- Use SQLAlchemy 2.0+ syntax
- Store SQLite database in `data/database/etex.db` (gitignored)
- Create models in `src/backend/models/`

## Week / Phase
Week 1 / MVP Phase 1

## Dependencies
- None (first task)

## Blocks
- #16 (Alembic migrations)
- #17 (API endpoints)

## Estimated Effort
🔶 Large (1-2 days)
```

**Assignee**: Your GitHub username
**Project**: ETEx MVP - 6 Week Sprint
**Custom Fields**:
- Week: `Week 1`
- Effort: `🔶 Large`
- Component: `Database`

---

### Example 2: Week 2 Bug Issue

**Title**: `bug(extraction): PDF parser fails on scanned NAMUR NE107 documents`

**Labels**: `type: bug`, `priority: high`, `phase: mvp`, `component: extraction`

**Description**:
```markdown
## Bug Description
When uploading scanned NAMUR NE107 PDF (image-based, no text layer), the PDF extractor crashes instead of gracefully handling unsupported format.

## Steps to Reproduce
1. Upload `tests/fixtures/namur-ne107-scanned.pdf`
2. Click "Extract Terms" button
3. Observe error in console

## Expected Behavior
Should detect image-based PDF and show error message:
"This PDF is scanned (image-only). OCR support coming in Phase 2. Please provide text-based PDF."

## Actual Behavior
Crashes with:
```
IndexError: list index out of range
  File "src/backend/services/extraction/pdf_processor.py", line 45
```

## Error Log
```
[2025-10-31 14:32:15] ERROR: PDF extraction failed
Traceback (most recent call last):
  ...
IndexError: list index out of range
```

## Environment
- Python 3.12.0
- Windows 11
- pdf_extractor.py from Glossary APP (vendored)

## Impact
🟠 High - Affects Week 2 milestone, but scanned PDFs are edge case (5% of docs)

## Proposed Fix
1. Add `is_scanned_pdf()` check before extraction
2. Return friendly error message if scanned
3. Add unit test for scanned PDF handling
4. Document limitation in docs/REQUIREMENTS.md (MVP exclusion)

## Related Issues
- Blocks #18 (Week 2 completion)
- Future: #45 (Phase 2C - OCR support)
```

**Assignee**: Your GitHub username
**Project**: ETEx MVP - 6 Week Sprint
**Custom Fields**:
- Week: `Week 2`
- Effort: `🔹 Small`
- Component: `Extraction`

---

### Example 3: Week 4 Documentation Issue

**Title**: `docs(wiki): Add IATE API integration setup guide with examples`

**Labels**: `type: docs`, `priority: medium`, `phase: mvp`, `component: api-integration`

**Description**:
```markdown
## What Needs Documentation
Complete setup guide for IATE API integration including authentication, rate limits, and example requests/responses.

## Target Audience
- Developers setting up ETEx for first time
- Users configuring IATE API credentials
- Future contributors adding new authoritative sources

## Location
GitHub Wiki > Developer Guide > IATE API Integration

## Content Needed
1. **Prerequisites**
   - IATE API account creation (link to EU portal)
   - API key generation steps (with screenshots)

2. **Configuration**
   - `.env` file setup (IATE_API_KEY, IATE_API_ENDPOINT)
   - Example `.env` values

3. **Testing Connection**
   - How to run `scripts/test-iate-connection.py`
   - Expected output (success/failure)

4. **API Examples**
   - Search for term "pressure sensor" in German/English
   - Request/response JSON examples
   - Error handling (rate limit, invalid credentials)

5. **Troubleshooting**
   - Common errors ("401 Unauthorized", "429 Too Many Requests")
   - Solutions for each

## Related Code
- `src/backend/services/iate_client.py`
- `.env.example`
- `docs/REQUIREMENTS.md` section 6.1 (Module Type A)

## Week / Phase
Week 4 / MVP Phase 1

## Estimated Effort
🔸 Medium (4-6 hours)
```

**Assignee**: Your GitHub username
**Project**: ETEx MVP - 6 Week Sprint
**Custom Fields**:
- Week: `Week 4`
- Effort: `🔸 Medium`
- Component: `API Integration`

---

### Example 4: Planning Update via Issue

**Title**: `planning: Update Week 3 scope - defer synonym auto-linking to Phase 2`

**Labels**: `type: chore`, `priority: medium`, `phase: mvp`

**Description**:
```markdown
## Change Proposal
Move synonym auto-linking from Week 3 (MVP) to Phase 2E (post-MVP).

## Rationale
Week 3 is overloaded:
- Term extraction is more complex than estimated (handling multi-language PDFs)
- Manual synonym linking via UI is sufficient for MVP
- Auto-detection requires NLP (spaCy embeddings) = extra complexity

## Impact on MVP
✅ **MVP still achieves goal**: Users can manually link synonyms via UI
❌ **No auto-detection**: Users must identify synonyms themselves (acceptable for MVP)

## Updated Week 3 Scope
**Remove**:
- [ ] Synonym auto-detection algorithm
- [ ] spaCy word embeddings
- [ ] Co-occurrence analysis

**Keep**:
- [x] Term extraction from PDFs
- [x] Manual term review UI
- [x] Manual synonym linking UI (admin creates links)

## Updated docs/REQUIREMENTS.md
Section 10 (MVP Scope) - move synonym auto-detection to EXCLUDES list.

## Dependencies
- Update #22 (Week 3 tasks) to remove auto-detection subtasks
- Create #67 (Phase 2E - Synonym Auto-Detection)

## Approval Needed
Please review and comment if this scope change is acceptable.
```

**Labels**: `type: planning`, `priority: medium`, `phase: mvp`
**Assignee**: Your GitHub username
**Status**: `status: planning`

---

### Example 5: Pull Request for Week 1 Completion

**Title**: `feat(backend): Implement database schema and Alembic migrations (Week 1)`

**PR Description**:
```markdown
## Summary
Implements the 5 core database tables (authoritative_sources, terms, term_synonyms, translations, uploaded_documents) using SQLAlchemy ORM and sets up Alembic migrations.

## Changes Made
- Created SQLAlchemy models in `src/backend/models/`:
  - `authoritative_source.py` (12 fields, tier enum, config JSON)
  - `term.py` (14 fields, full-text search index, language validation)
  - `term_synonym.py` (bidirectional relationship, confidence scoring)
  - `translation.py` (source/target language validation)
  - `uploaded_document.py` (file tracking, processing status)
- Setup Alembic migrations (`alembic/versions/001_initial_schema.py`)
- Added database config in `src/backend/core/database.py`
- Created `.env.example` with database URL
- Added unit tests for models (95% coverage)

## Related Issues
Closes #15 (Database schema)
Closes #16 (Alembic setup)
Blocks #17 (API endpoints - Week 2)

## Testing
- [x] Unit tests pass (`pytest tests/unit/backend/models/`)
- [x] Migration runs successfully (`alembic upgrade head`)
- [x] Database created at `data/database/etex.db`
- [x] Coverage: 95% (target: 80%)
- [x] Manual testing: Created sample data, verified relationships

## Code Reuse
- Referenced `vendor/glossary-app/src/backend/models/base_models.py` for pattern (Tier 3)
- No code copied (implemented from scratch based on requirements)

## Review Checklist
- [x] Code follows PEP 8 (checked with `black` and `flake8`)
- [x] All foreign keys have proper cascade behavior
- [x] Indexes added for performance (verified with `EXPLAIN QUERY PLAN`)
- [x] No hardcoded secrets (database URL from `.env`)
- [x] Error handling for invalid data (tested with malformed inputs)
- [x] Documentation updated (README.md database section)

## Database Schema Verification
```sql
-- Verified all 5 tables created:
SELECT name FROM sqlite_master WHERE type='table';
-- Output: authoritative_sources, terms, term_synonyms, translations, uploaded_documents

-- Verified indexes created:
SELECT name FROM sqlite_master WHERE type='index';
-- Output: idx_terms_language, idx_terms_source, idx_translations_source_lang, ...
```

## Next Steps
- Week 2: API endpoints for CRUD operations
- Week 2: PDF upload and extraction integration
```

**Assignee**: Your GitHub username
**Reviewers**: Self-review (or Review Agent if multi-agent)
**Labels**: `type: feature`, `phase: mvp`, `component: database`
**Linked Issues**: Closes #15, Closes #16

---

## Recommended Setup Sequence

### Week 0 (Setup Week - This Week!)

1. **Create Issue Templates** (`.github/ISSUE_TEMPLATE/`)
   - `feature_request.yml`
   - `bug_report.yml`
   - `documentation.yml`

2. **Create Labels** (via GitHub UI or `gh` CLI)
   - Type labels (feature, bug, docs, etc.)
   - Priority labels (critical, high, medium, low)
   - Component labels (backend, frontend, database, etc.)
   - Phase labels (mvp, phase-2a, future)

3. **Setup GitHub Project Board**
   - Create "ETEx MVP - 6 Week Sprint" project
   - Add Kanban view (Backlog → Design → Ready → In Progress → Review → Done)
   - Add Timeline view (Week 1-6)
   - Add Table view (all custom fields)

4. **Create Week 1-6 Milestone Issues**
   - Issue #1: Week 1 - Project Setup & Database
   - Issue #2: Week 2 - Document Upload & PDF Processing
   - Issue #3: Week 3 - Term Extraction & Storage
   - Issue #4: Week 4 - IATE API Integration
   - Issue #5: Week 5 - IEC Database Import & Search
   - Issue #6: Week 6 - Manual Entry, Browse & Polish

5. **Populate Initial Issues** (from docs/REQUIREMENTS.md)
   - Break down Week 1 tasks into individual issues
   - Assign to Week 1 milestone
   - Add to project board

6. **Setup GitHub Wiki** (optional for now, can wait until Week 2-3)
   - Create Home page
   - Mirror `docs/getting-started/SETUP.md`

---

## Best Practices

### 1. **Issue Hygiene**
- ✅ One issue = one task (atomic, completable)
- ✅ Close issues when done (don't leave stale open issues)
- ✅ Link issues to PRs (`Closes #15` in PR description)
- ✅ Update issue status when moving between stages

### 2. **Labeling**
- Always add: Type + Priority + Phase + Component
- Example: `type: feature`, `priority: high`, `phase: mvp`, `component: backend`

### 3. **Descriptions**
- Use templates (consistent structure)
- Add acceptance criteria (testable)
- Link related issues/PRs
- Estimate effort (helps planning)

### 4. **Project Board**
- Move issues manually or use automation
- Review board weekly (what's blocked? what's done?)
- Use Timeline view for week-by-week visualization

### 5. **Pull Requests**
- Always link to issues (`Closes #15`)
- Fill out description template
- Self-review before merging (even solo)
- Squash commits if messy history

---

## Quick Reference: Common Commands

### Create Issue
```bash
gh issue create --title "feat(backend): Add search API endpoint" \
  --body "..." \
  --label "type: feature,priority: high,component: backend" \
  --milestone "Week 5"
```

### List Issues
```bash
gh issue list --label "phase: mvp" --state open
```

### Close Issue
```bash
gh issue close 15 --comment "Completed in PR #23"
```

### Create PR
```bash
gh pr create --title "feat(backend): Add search API" \
  --body "Closes #15" \
  --label "type: feature"
```

### View Project
```bash
gh project view 1
```

---

## Questions & Answers

**Q: Should every task have an issue?**
A: For MVP, yes! Small tasks (< 1 hour) can share an issue. Example: "Week 1 setup tasks" issue with checklist.

**Q: Do I need to use PRs if working solo?**
A: Optional, but **recommended**. PRs create better documentation and GitHub UI catches mistakes.

**Q: When should I update the Wiki vs repo docs?**
A: Update repo `docs/` first (source of truth), then optionally mirror to Wiki for discoverability.

**Q: Can I change the roadmap via issue?**
A: Yes! Create `type: planning` issue, discuss changes, update `docs/REQUIREMENTS.md`, close issue.

**Q: How do I handle blocking dependencies?**
A: Add `status: blocked` label, comment with reason, link to blocking issue.

---

## Success Metrics

This workflow succeeds when:
- ✅ Every task is tracked (no "lost" work)
- ✅ Progress is visible (board shows what's done/in-progress)
- ✅ Issues are discoverable (good titles, labels, descriptions)
- ✅ History is clear (commits link to issues, PRs explain changes)
- ✅ Collaboration is smooth (if multi-agent or team grows)

---

**End of GitHub Workflow Guide**
**Last Updated**: 2025-10-31
**Version**: 1.0
