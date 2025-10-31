# ETEx - Claude Agent Guidelines

**Project**: ETEx (Engineering Terminology Explorer)
**Purpose**: Multi-language terminology search and translation system across industry standards
**Reference Project**: Glossary APP (located at `vendor/glossary-app/`)

---

## Project Context

Building ETEx using proven components from the Glossary APP project. The goal is to **reference and reuse** existing, battle-tested code rather than copying or rewriting from scratch.

**Core Problem We're Solving**: German source documents use inconsistent terminology (e.g., "Drucksensor" vs "Druckmessumformer"), leading to translation errors downstream.

**Solution**: Build a language-internal thesaurus that maps synonyms within each language, and match terminology across regional/international standards (NAMUR ↔ IATE ↔ DIN ↔ IEC).

---

## Global Rules (All Roles)

### Code Reuse Strategy

**Priority Order**:
1. **Check vendor/ first**: Before writing new code, check if it exists in `vendor/glossary-app/`
2. **Import when possible** (Tier 1): Direct import from vendor
   ```python
   from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor
   ```
3. **Copy with attribution** (Tier 2): When modifications needed
   ```python
   """
   Adapted from Glossary APP (2025-10-31)
   Original: vendor/glossary-app/src/backend/services/pdf_extractor.py
   Modifications:
   - Added IEC Electropedia specific PDF parsing
   - Changed page reference format for authoritative sources
   """
   ```
4. **Reference only** (Tier 3): Document in `docs/reference/` for inspiration

**See**: [docs/reference/code-reuse-strategy.md](docs/reference/code-reuse-strategy.md) for complete guide

### Progress Tracking

**DON'T**:
- ❌ Create or update manual status files (`.progress/status.md`) - they go stale
- ❌ Maintain separate todo lists - use git and issues

**DO**:
- ✅ Make descriptive git commits with context
- ✅ Update GitHub Issues/Project board (if available)
- ✅ Write ADRs (Architecture Decision Records) for major decisions in `docs/adr/`
- ✅ Use commit messages to track progress

**Example git commit**:
```bash
git commit -m "feat(extraction): Implement PDF extraction for NAMUR standards

- Integrated pdf_extractor.py from Glossary APP
- Added IEC-specific page reference format
- Tests cover malformed PDFs and encoding errors
- Progress: Week 2 - 60% complete"
```

### Documentation Standards

**Where things go**:
- **Architecture docs**: `docs/architecture/` - System design, database schemas, API contracts
- **ADRs**: `docs/adr/` - Important decisions (immutable once accepted)
- **Reference guides**: `docs/reference/` - How to reuse Glossary APP components
- **Setup guides**: `docs/getting-started/` - Installation, troubleshooting
- **Agent workspace**: `.agent/workspace/` - Temporary working files (gitignored)
- **Agent outputs**: `.agent/outputs/` - Completed artifacts for review (committed)

---

## Role Detection

**How to know your current role**:

1. **User tells you explicitly**:
   - "Act as the Design Agent..."
   - "Now switch to Coding Agent mode..."
   - "Review this code as the Review Agent..."

2. **Task type indicates role**:
   - Creating specs, mockups, architecture diagrams → **Design Role**
   - Writing code, tests, implementing features → **Coding Role**
   - Reviewing code, running tests, security audits → **Review Role**

3. **Working directory context**:
   - Working in `.agent/workspace/design/` → **Design Role**
   - Working in `.agent/workspace/coding/` → **Coding Role**
   - Working in `.agent/workspace/review/` → **Review Role**

---

## [Design Role] - When Designing Features

### Responsibilities
- Create feature specifications
- Design database schemas
- Create API contracts (OpenAPI/Swagger format)
- Draw architecture diagrams
- Research existing patterns in vendor/glossary-app/

### Workspace
- **Working files**: `.agent/workspace/design/`
- **Final specs**: `docs/architecture/`
- **Decisions**: `docs/adr/`

### Process

1. **Research Phase**
   - Check `vendor/glossary-app/` for similar features
   - Review existing specs in `docs/architecture/`
   - Read relevant ADRs in `docs/adr/`

2. **Draft Phase**
   - Create spec draft in `.agent/workspace/design/`
   - Include:
     - Feature overview and acceptance criteria
     - Database schema with constraints/indexes
     - API contracts with example requests/responses
     - UI/UX mockups (if applicable)
     - Security requirements
     - Testing strategy

3. **Review Phase**
   - Self-review against quality checklist
   - Verify spec is implementation-ready (no ambiguity)

4. **Finalize Phase**
   - Move final spec to `docs/architecture/`
   - Create ADR if major architectural decision
   - Update GitHub Issue: "Design complete, ready for coding"

### Quality Checklist

Before marking design complete:
- [ ] Specification is implementation-ready (coding agent can start without questions)
- [ ] API contracts have example requests/responses with status codes
- [ ] Database schema includes all constraints, indexes, and foreign keys
- [ ] Security requirements are explicit (auth, validation, XSS prevention, etc.)
- [ ] Testing strategy is defined (unit/integration/e2e scope)
- [ ] Reusable components from vendor/ identified and documented
- [ ] Error handling specified (what errors, what HTTP codes, what messages)

### Example Workflow

```bash
# 1. Research in vendor/
cd vendor/glossary-app/
ls src/backend/services/  # See what's available

# 2. Draft spec
cd .agent/workspace/design/
vim feature-001-pdf-upload-spec.md
# Write comprehensive specification

# 3. Finalize
mv feature-001-pdf-upload-spec.md ../../../docs/architecture/
cd ../../../

# 4. Create ADR if needed
cp docs/adr/template.md docs/adr/0002-use-fastapi-file-upload.md
vim docs/adr/0002-use-fastapi-file-upload.md

# 5. Commit
git add docs/architecture/feature-001-pdf-upload-spec.md
git add docs/adr/0002-use-fastapi-file-upload.md
git commit -m "docs: Add PDF upload specification

- API endpoints defined
- File validation strategy
- Storage approach decided (ADR-0002)
- Ready for implementation"
```

---

## [Coding Role] - When Implementing Features

### Responsibilities
- Implement features per specification
- Write tests (target: 80%+ coverage)
- Import/adapt code from vendor/glossary-app/
- Follow coding standards
- Ensure all tests pass before handoff

### Workspace
- **Working files**: `.agent/workspace/coding/`
- **Final code**: `src/`
- **Tests**: `tests/`

### Process

1. **Preparation Phase**
   - Read spec from `docs/architecture/`
   - Check `vendor/glossary-app/` for reusable components
   - Identify Tier 1 (import) vs Tier 2 (copy) components

2. **Implementation Phase**
   - Write tests first (Test-Driven Development)
   - Implement feature according to spec
   - Import from vendor/ when possible (Tier 1)
   - Copy with attribution when modifications needed (Tier 2)
   - Follow spec exactly - if spec is wrong, ask Design Agent to update it

3. **Testing Phase**
   - Run all tests (unit + integration)
   - Check test coverage (target: 80%+)
   - Manual testing of critical paths
   - **If bugs/issues found**: Create GitHub Issue immediately (see Bug Tracking section below)
   - Fix any issues

4. **Finalize Phase**
   - Run linting
   - Ensure all tests pass
   - Create descriptive commit message
   - Update GitHub Issue: "Implementation complete, ready for review"

### Code Attribution Template

**When copying code (Tier 2)**:
```python
"""
Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/pdf_extractor.py
Modifications:
- Added IEC Electropedia specific PDF parsing rules
- Modified page reference extraction for standards documents
- Added support for multilingual PDF metadata
"""

class PDFExtractor:
    # ... implementation ...
```

### Quality Checklist

Before marking implementation complete:
- [ ] All spec requirements implemented
- [ ] Code passes linting (`flake8`, `black`, `pylint`)
- [ ] All tests pass (unit + integration)
- [ ] Test coverage ≥ 80%
- [ ] Attribution headers on all copied code (Tier 2)
- [ ] No hardcoded secrets or credentials
- [ ] Error handling implemented per spec
- [ ] Descriptive git commit message written

### Example Workflow

```bash
# 1. Read spec
cat docs/architecture/feature-001-pdf-upload-spec.md

# 2. Check vendor for reusable code
ls vendor/glossary-app/src/backend/services/
# Found: pdf_extractor.py

# 3. Decide: Import (Tier 1) or Copy (Tier 2)?
# Decision: Import as-is (no modifications needed)

# 4. Implement
cd src/backend/services/
vim document_processor.py

# Import directly (Tier 1)
cat > document_processor.py << 'EOF'
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

class DocumentProcessor:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()

    def process_upload(self, file_path):
        return self.pdf_extractor.extract(file_path)
EOF

# 5. Write tests
cd ../../../tests/unit/backend/
vim test_document_processor.py

# 6. Run tests
cd ../../..
pytest tests/unit/backend/test_document_processor.py --cov

# 7. Commit
git add src/backend/services/document_processor.py
git add tests/unit/backend/test_document_processor.py
git commit -m "feat(extraction): Implement document processor

- Reused pdf_extractor.py from Glossary APP (Tier 1 import)
- Added tests with 85% coverage
- All tests passing
- Ready for review"
```

---

## Bug Tracking & GitHub Issues

### When to Create a GitHub Issue

**MANDATORY** - Create a GitHub Issue when:
1. **Bug discovered during testing** - Any bug found during development or review
2. **Bug discovered during implementation** - Unexpected behavior, crashes, errors
3. **Security vulnerability found** - Input validation missing, XSS, SQL injection, etc.
4. **Performance issue detected** - Slow queries, memory leaks, response time > 500ms
5. **Test failures** - Tests failing that previously passed (regression)
6. **Edge case discovered** - Unhandled scenario found during manual testing
7. **Third-party integration issue** - API errors, vendor code bugs, dependency issues

**Do NOT create issue for**:
- Typos in code comments (just fix inline)
- Minor code style issues caught by linter (just fix inline)
- Simple refactoring opportunities (unless blocking, then create issue)

### How to Create Bug Issues

**Use the bug report template**:

```bash
gh issue create --template bug_report.yml \
  --title "bug(component): Brief description" \
  --label "type: bug,priority: high,component: backend"
```

**Or via web**: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=bug_report.yml

**Required Information**:
- **Component**: Where did bug occur? (backend, frontend, database, extraction)
- **Impact**: Critical (blocks MVP), High (core functionality), Medium (workaround), Low (edge case)
- **Steps to reproduce**: Exact steps to trigger bug
- **Expected vs Actual behavior**: What should happen vs what actually happens
- **Error log**: Stack trace, error messages, console output
- **Environment**: Python version, OS, browser (if frontend)

### Bug Workflow

**1. Discover Bug** → **2. Create Issue** → **3. Fix** → **4. Close Issue**

**Example Workflow**:

```bash
# Step 1: Discover bug during testing
# Upload PDF → crashes with IndexError

# Step 2: Create GitHub Issue
gh issue create \
  --title "bug(extraction): PDF parser crashes on scanned documents" \
  --label "type: bug,priority: high,component: extraction" \
  --body "Steps to reproduce:
1. Upload scanned NAMUR PDF
2. Click Extract Terms
3. Crashes with IndexError

Expected: Show error message 'Scanned PDFs not supported'
Actual: Crashes with IndexError: list index out of range

Error log: [paste error]
Environment: Python 3.12, Windows 11"

# GitHub creates Issue #23

# Step 3: Fix the bug
git checkout -b fix/scanned-pdf-handling
# ... implement fix ...
git commit -m "fix(extraction): Handle scanned PDFs gracefully

- Added is_scanned_pdf() detection
- Return 400 error with friendly message
- Added unit test for scanned PDF handling

Fixes #23"

# Step 4: Issue automatically closed when PR merged
gh pr create --title "fix(extraction): Handle scanned PDFs (Fixes #23)"
gh pr merge --squash
# Issue #23 auto-closed
```

### Bug Priority Guidelines

**Priority: Critical** (Must fix immediately)
- Blocks MVP milestone
- Security vulnerability
- Data loss
- Complete feature breakdown
- System crash

**Priority: High** (Fix this week)
- Core functionality broken
- Affects multiple users
- No workaround available
- Blocks other development

**Priority: Medium** (Fix this sprint)
- Non-critical feature broken
- Workaround exists
- Affects edge cases
- Performance degradation

**Priority: Low** (Fix when convenient)
- Cosmetic issues
- Rare edge cases
- Minor inconvenience
- Enhancement ideas

### Issue Labels for Bugs

**Required labels** (3):
1. **Type**: `type: bug`
2. **Priority**: `priority: critical`, `priority: high`, `priority: medium`, or `priority: low`
3. **Component**: `component: backend`, `component: frontend`, `component: database`, `component: extraction`, or `component: api-integration`

**Optional labels**:
- `phase: mvp` - If blocks MVP
- `status: blocked` - If waiting on external dependency
- `status: in-progress` - If actively being fixed

### Bug Documentation

**After fixing, document in**:
1. **Git commit message**: Reference issue number (`Fixes #23`)
2. **CHANGELOG.md**: Add to "Fixed" section
3. **Tests**: Add regression test to prevent recurrence
4. **Code comments**: If tricky fix, explain why bug occurred

---

## Agent-Generated Issues

### When Agents Should Create Issues

**Design Agent** creates issues when:
- Spec has ambiguity or missing requirements (`type: design-issue`)
- User decision needed (`type: clarification`)
- Found conflicting requirements
- Discovered dependency on external API/service

**Coding Agent** creates issues when:
- Blocked by missing dependency (`type: blocked`)
- Spec is unclear or contradictory (`type: clarification`)
- Discovered bug during implementation (`type: bug`)
- Found edge case not covered in spec (`type: design-issue`)

**Review Agent** creates issues when:
- Found security vulnerability (`severity: critical`)
- Found code quality issues (`severity: major` or `severity: minor`)
- Suggests improvement (`severity: suggestion`)
- Tests are insufficient (`type: bug`)

**Explore Agent** creates issues when:
- Has question about codebase (`type: question`)
- Found interesting pattern to note (`type: observation`)
- Discovered potential improvement (`severity: suggestion`)

### Agent Issue Labels

**Required labels for agent issues** (minimum 3):
1. **Agent label**: `agent: design`, `agent: coding`, `agent: review`, or `agent: explore`
2. **Type label**: `type: bug`, `type: clarification`, `type: design-issue`, `type: blocked`, etc.
3. **Priority label**: `priority: critical`, `priority: high`, `priority: medium`, or `priority: low`

**Optional labels**:
- **Component**: `component: backend`, `component: frontend`, etc.
- **Severity** (review findings only): `severity: critical`, `severity: major`, `severity: minor`, `severity: suggestion`
- **Phase**: `phase: mvp` if blocks MVP

### Agent Issue Title Convention

```
<type>(<component>): <brief description> [agent-generated]
```

**Examples**:
- `clarification: IATE API authentication method unclear [agent-generated]`
- `bug(backend): SQL injection in search endpoint [agent-generated]`
- `blocked: spaCy German model not in requirements [agent-generated]`
- `observation: Better error handling pattern in vendor/ [agent-generated]`

### Agent Issue Best Practices

**DO**:
- ✅ Create issue immediately when finding blocking issue
- ✅ Provide clear context (file, line, what task you were doing)
- ✅ Suggest fix if you know the solution
- ✅ Use appropriate severity/priority labels
- ✅ Add `[agent-generated]` to title for tracking
- ✅ Report issue to user with actionable next steps

**DON'T**:
- ❌ Create issue for minor code style (just fix inline)
- ❌ Create duplicate issues (search first)
- ❌ Create issue without context or reproduction steps
- ❌ Forget to label with agent role
- ❌ Create issue without priority/severity

---

## [Review Role] - When Reviewing Code

### Responsibilities
- Review code for functionality, quality, security
- Run full test suite
- Security audit (input validation, auth, XSS, SQL injection)
- Verify spec compliance
- Either approve or create detailed fix list

### Workspace
- **Working files**: `.agent/workspace/review/`
- **Review reports**: `.agent/outputs/review/`
- **Fix lists**: `.agent/outputs/review/fixes/`

### Process

1. **Preparation Phase**
   - Read implementation from `src/`
   - Read original spec from `docs/architecture/`
   - Read test files from `tests/`

2. **Code Review Phase**
   - **Functionality**: Does it meet all spec requirements?
   - **Code Quality**: Is it readable, maintainable, follows standards?
   - **Security**: Input validation? Auth? XSS prevention? SQL injection?
   - **Performance**: Database queries optimized? Response times acceptable?
   - **Testing**: Adequate coverage? Tests are maintainable?
   - **Attribution**: Copied code has proper headers?

3. **Testing Phase**
   - Run unit tests: `pytest tests/unit/ --cov`
   - Run integration tests: `pytest tests/integration/`
   - Check coverage report
   - Run security scanners if available

4. **Decision Phase**
   - **If approved**: Create approval document, update issue
   - **If fixes needed**: Create detailed fix list with severity levels

### Review Checklist

- [ ] **Functionality**: All spec requirements met
- [ ] **Code Quality**: Readable, follows conventions, no duplication
- [ ] **Security**: Input validation, auth checks, no XSS/SQL injection
- [ ] **Performance**: Queries optimized, response times acceptable
- [ ] **Testing**: 80%+ coverage, tests pass, good test quality
- [ ] **Attribution**: Tier 2 copied code has proper headers
- [ ] **Documentation**: Code is documented, complex logic explained
- [ ] **Error Handling**: Errors caught, logged, user-friendly messages

### Fix Severity Levels

- **CRITICAL**: Must fix before approval (security issues, broken functionality)
- **MAJOR**: Should fix (poor performance, missing tests, quality issues)
- **MINOR**: Nice to have (code style, minor optimizations)

### Example Review Report Template

Save to `.agent/outputs/review/feature-001-review.md`:

```markdown
# Code Review Report: Feature 001 - PDF Upload

**Reviewer**: Review Agent
**Date**: 2025-10-31
**Commit**: abc1234
**Status**: ⚠️ NEEDS FIXES

---

## Summary

Implementation is mostly solid, but found 1 CRITICAL security issue and 2 MAJOR code quality issues that must be addressed before approval.

---

## Functionality Review: ✅ PASS

- ✅ All API endpoints implemented per spec
- ✅ File upload works correctly
- ✅ PDF extraction integrated properly

---

## Security Review: ❌ FAIL

### Issues Found

1. **[CRITICAL]** Missing file type validation
   - **Location**: `src/backend/api/documents.py:45`
   - **Problem**: Accepts any file type, not just PDFs
   - **Risk**: Could allow upload of malicious executables
   - **Fix**: Add file extension whitelist: `['.pdf']`
   ```python
   if not filename.endswith('.pdf'):
       raise HTTPException(400, "Only PDF files allowed")
   ```

---

## Code Quality Review: ⚠️ ISSUES

### Issues Found

2. **[MAJOR]** No test for file validation
   - **Location**: `tests/unit/backend/test_documents.py`
   - **Problem**: Missing tests for invalid file types
   - **Fix**: Add test cases for `.exe`, `.txt`, `.docx` uploads

3. **[MAJOR]** Hardcoded file path
   - **Location**: `src/backend/services/document_processor.py:23`
   - **Problem**: Upload path hardcoded to `C:/uploads/`
   - **Fix**: Use config variable from environment

---

## Testing Review: ⚠️ PASS (with gaps)

- ✅ Unit test coverage: 82%
- ⚠️ Missing edge case tests (invalid file types)
- ✅ Integration tests present

---

## Decision: ⚠️ NEEDS FIXES

**Required Fixes**:
1. Fix CRITICAL security issue (file type validation)
2. Add tests for file validation
3. Remove hardcoded upload path

**Estimated Fix Time**: 1-2 hours

**Next Steps**:
1. Coding agent applies fixes
2. Re-submit for review (focused re-review of fixes only)

---

**Reviewed by**: Review Agent
**Date**: 2025-10-31
```

---

## Multi-Agent Mode (3 Parallel Instances)

**If running 3 Claude Code instances simultaneously**:

### Agent Workspaces

Each agent works in their own workspace to avoid conflicts:

```
.agent/workspace/
├── design/       # Design agent workspace
├── coding/       # Coding agent workspace
└── review/       # Review agent workspace
```

### Handoff Protocol

**Design → Coding Handoff**:
1. Design agent: Move spec to `docs/architecture/`
2. Design agent: Git commit with message "docs: Feature X spec ready for coding"
3. Design agent: Update GitHub Issue: "Ready for Coding"
4. Coding agent: Pull latest changes, read spec, start implementation

**Coding → Review Handoff**:
1. Coding agent: Commit code with message "feat: Feature X implementation ready for review"
2. Coding agent: Update GitHub Issue: "Ready for Review"
3. Review agent: Pull latest changes, review code, run tests

**Review → Coding (if fixes needed)**:
1. Review agent: Create fix list in `.agent/outputs/review/fixes/`
2. Review agent: Update GitHub Issue: "Needs Fixes - see review report"
3. Coding agent: Read fix list, apply fixes, re-submit

### Conflict Prevention

**File Ownership Rules**:
- Design agent: OWNS `docs/architecture/`, `docs/adr/`, `.agent/workspace/design/`
- Coding agent: OWNS `src/`, `tests/`, `.agent/workspace/coding/`
- Review agent: OWNS `.agent/workspace/review/`, `.agent/outputs/review/`
- All agents: CAN READ everything, but respect ownership for writes

**Progress Communication**:
- Use git commits (automatic timestamps, clear history)
- Use GitHub Issues/Project boards (visual tracking)
- Don't rely on shared status files (merge conflicts)

---

## Common Tasks

### Reusing Glossary APP Code

**See**: [docs/reference/code-reuse-strategy.md](docs/reference/code-reuse-strategy.md)

**Quick Reference**:

**Check what's available**:
```bash
ls vendor/glossary-app/src/backend/services/
ls vendor/glossary-app/src/frontend/src/components/
```

**Tier 1 - Import directly** (preferred):
```python
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor
```

**Tier 2 - Copy with attribution** (when modifications needed):
```python
"""
Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/term_extractor.py
Modifications:
- Extracted only clean_term() and strip_leading_articles() utilities
- Removed spaCy dependency for lightweight deployment
"""
# ... copied code ...
```

**Tier 3 - Reference only** (inspiration):
Document in `docs/reference/` for future reference

---

### Creating Architecture Decision Record (ADR)

**When to create an ADR**:
- Choosing technology stack
- Major architectural changes
- Security approach decisions
- Database schema major changes
- API design patterns

**Process**:
```bash
# 1. Copy template
cp docs/adr/template.md docs/adr/0003-my-decision.md

# 2. Fill out template
# - Context: Why are we deciding this?
# - Decision: What did we choose?
# - Consequences: What becomes easier/harder?

# 3. Commit
git add docs/adr/0003-my-decision.md
git commit -m "docs: Add ADR for [decision topic]"
```

---

### Updating Progress

**Preferred method**: Git commits + GitHub Issues

**Git commit template**:
```bash
git commit -m "feat(module): Brief summary of change

- Detail 1
- Detail 2
- Progress: Week X - Y% complete
- Closes #issue-number (if applicable)"
```

**GitHub Issue update**:
- Comment with status: "Implementation 60% complete, API endpoints done, tests in progress"
- Move card on project board (Backlog → In Progress → Done)
- Assign yourself if working on it

---

## Anti-Patterns (DON'T DO THIS)

### ❌ Copying code without attribution

**Bad**:
```python
class PDFExtractor:
    # Where did this come from? Who wrote it? Can we modify it?
    ...
```

**Good**:
```python
"""
Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/pdf_extractor.py
Modifications: None (using as-is)
"""
class PDFExtractor:
    ...
```

---

### ❌ Creating manual status files

**Bad**:
```markdown
# .progress/status.md (will go stale, merge conflicts)
Feature X: In Progress (60%)
Feature Y: Done
```

**Good**:
```bash
# Use git commits (automatic timestamps, full history)
git commit -m "feat(search): Implement search API (60% complete)

- Basic search endpoint working
- Tests added
- TODO: Pagination and filters"
```

---

### ❌ Skipping design phase for complex features

**Bad**:
```
User: "Build authentication system"
You: [Immediately writes code without spec]
```

**Good**:
```
User: "Build authentication system"
You: [Design role] "Let me create a specification first. I'll design:
      - JWT token structure
      - Token refresh flow
      - Session management
      - API endpoints
      Then we can implement it correctly."
```

---

### ❌ Implementing before reading spec

**Bad**:
```python
# Coding agent starts writing auth without reading design spec
# Ends up with different JWT structure than designed
```

**Good**:
```bash
# 1. Read spec first
cat docs/architecture/feature-auth-spec.md

# 2. Understand requirements completely
# 3. Then implement exactly per spec
```

---

### ❌ Approving code without running tests

**Bad**:
```
Review agent: "Code looks good! Approved."
[Never ran tests, missed broken functionality]
```

**Good**:
```bash
# Review agent runs full test suite
pytest tests/ --cov

# Checks coverage
# Tests manually
# Then approves
```

---

## Questions & Answers

**Q: Can I work without git submodules for vendor/?**
A: Yes, but document the Glossary APP code location clearly in `docs/reference/`. Git submodules are cleaner and keep the reference explicit.

**Q: What if I'm not sure which role to use?**
A: Ask the user: "Should I design this feature first (create spec), or implement it directly (if spec already exists)?"

**Q: Do I always need to follow the full Design → Code → Review process?**
A:
- **Complex features**: Yes (new features, architectural changes)
- **Simple bug fixes**: No (just fix, test, commit)
- **Code refactoring**: Usually yes (design the refactoring approach first)
- Use judgment based on complexity

**Q: What if the spec is wrong or unclear?**
A:
- **Coding agent**: Don't guess! Ask Design agent to clarify/update spec
- **Don't implement based on assumptions**
- Post question in `.agent/workspace/coding/questions.md` if multi-agent mode

**Q: How do I sync vendor/glossary-app/ with latest changes?**
A:
```bash
git submodule update --remote vendor/glossary-app
git add vendor/glossary-app
git commit -m "chore: Update Glossary APP reference to latest"
```

**Q: Can I modify code in vendor/?**
A: **NO**. vendor/ is read-only reference. If you need modifications:
- Copy to `src/` (Tier 2)
- Add attribution header
- Make your modifications
- Consider contributing fixes back to Glossary APP

---

## Success Metrics

**This workflow succeeds when**:
- ✅ New developers understand the structure in < 30 minutes
- ✅ Simple tasks take < 5 minutes (no unnecessary ceremony)
- ✅ Complex tasks have clear workflow (Design → Code → Review)
- ✅ Code attribution is always clear (know what came from where)
- ✅ Git history tells the full story (no lost context)
- ✅ No manual status files going stale

---

**End of CLAUDE.md**
**Last Updated**: 2025-10-31
**Version**: 1.0
