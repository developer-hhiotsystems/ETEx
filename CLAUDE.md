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
- **Agent workspace**: `.agents/workspace/` - Temporary working files (gitignored)
- **Agent outputs**: `.agents/outputs/` - Completed artifacts for review (committed)

### Check Before Creating Folders/Files - MANDATORY

**Before creating ANY new folder or file structure, you MUST check for existing similar structures.**

**Procedure**:

1. **Search for existing patterns**:
   ```bash
   # Check for similar folder names
   ls -la | grep "<keyword>"

   # Find similar folders (up to 2 levels deep)
   find . -type d -name "*<keyword>*" -maxdepth 2

   # Example: Before creating .agents/, check for .agent*
   ls -la | grep "\.agent"
   ```

2. **Decision tree**:

   **If similar structure found**:
   - Analyze existing content (`ls -R <folder>`)
   - Determine if duplicate or legitimate separate structure
   - **If duplicate**: Consolidate into existing folder, do NOT create new one
   - **If ambiguous**: Ask user which to keep

   **If no similar structure found**:
   - Proceed with creation
   - Document in commit message why new structure was needed

   **If potential typo** (e.g., `.agent` vs `.agents`, `doc` vs `docs`):
   - ALWAYS ask user for clarification before creating

3. **Examples**:

   **Example 1 - Duplicate Prevention**:
   ```bash
   # Agent wants to create .agents/ folder
   ls -la | grep "\.agent"
   # Output: drwxr-xr-x .agent/

   # STOP - Similar folder exists!
   ls -R .agent/
   # Output: README.md, workspace/, outputs/

   # Analysis: .agent/ and .agents/ would be duplicates
   # Decision: Use existing .agent/ OR consolidate into .agents/
   # Action: Ask user OR analyze and consolidate
   ```

   **Example 2 - Legitimate New Folder**:
   ```bash
   # Agent wants to create scripts/data/ folder
   ls scripts/
   # Output: app/, dev/, docs/

   # No "data" or similar found
   # Decision: Legitimate new category
   # Action: Create scripts/data/ and document purpose
   ```

   **Example 3 - Ambiguous Case**:
   ```bash
   # Agent wants to create docs/api/
   ls -R docs/
   # Output: docs/architecture/, docs/reference/, docs/adr/

   # Question: Should API docs go in architecture/ or separate api/?
   # Decision: ASK USER
   ```

**Enforcement**:
- ❌ **Violation**: Creating duplicate folders without checking
- ⚠️ **Severity**: CRITICAL - requires immediate fix
- ✅ **Correction**: Delete duplicate, consolidate content, update all references

**Why This Rule Exists**:
- Prevents confusion (.agent vs .agents, doc vs docs)
- Maintains clean project structure
- Prevents broken references in documentation
- Industry best practice

### Scripts Organization - MANDATORY RULES

**CRITICAL REQUIREMENT**: Every PowerShell/Bash script MUST have its own subfolder with its own README.md

**Correct Structure**:
```
scripts/dev/github/
├── README.md                          # Category overview only
├── create-labels/
│   ├── create-labels.ps1             # The script
│   └── README.md                      # Script-specific guide
└── create-milestones/
    ├── create-milestones.ps1
    └── README.md
```

**WRONG Structure** (DO NOT DO THIS):
```
scripts/dev/github/
├── README.md
├── create-labels.ps1          ❌ NO! Must be in subfolder
├── create-milestones.ps1      ❌ NO! Must be in subfolder
└── helper-script.ps1          ❌ NO! Must be in subfolder
```

**Rules for Script Management**:

1. ✅ **Creating new script**:
   - Create subfolder: `scripts/<category>/<script-name>/`
   - Add script file: `<script-name>.ps1` or `<script-name>.sh`
   - Add README.md with purpose, usage, examples, troubleshooting
   - Update category README.md to list new script

2. ✅ **Updating existing script**:
   - Update the script file in its subfolder
   - Update its README.md with any usage changes
   - Update version/date in script header

3. ✅ **Script with new purpose (similar to existing)**:
   - Delete old script entirely (subfolder + README)
   - Create new subfolder with enhanced script
   - Document what changed in new README

4. ✅ **Script with new purpose (different from existing)**:
   - Keep old script if still useful
   - Create new subfolder for new script
   - Each script remains independent

5. ❌ **NEVER put multiple .ps1/.sh files directly in category folder**
   - Each script needs isolation for clarity
   - Users should find one folder = one script = one purpose

**Exception**: Application scripts (`scripts/app/`) MAY be less strict about subfolders for very simple runtime scripts (discuss with user first).

**Why This Rule Exists**:
- Clear organization: One folder = one purpose
- Easy discovery: README explains each script
- Version control: Clear history per script
- Reusability: Users can copy entire script folder with docs
- Professional: Industry standard for script repositories

**See**: [docs/reference/scripts-organization.md](docs/reference/scripts-organization.md) for complete guide

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
   - Working in `.agents/workspace/design/` → **Design Role**
   - Working in `.agents/workspace/coding/` → **Coding Role**
   - Working in `.agents/workspace/review/` → **Review Role**

---

## CRITICAL: Pre-Task Agent Check (MANDATORY)

**BEFORE starting ANY task, you MUST perform this 4-step check:**

### Step 1: Identify Task Type

Ask yourself these questions:

**Is this a backend task?**
- Python/FastAPI development
- Database models (SQLAlchemy)
- API endpoints
- Business logic
→ **Use Backend Expert**

**Is this a frontend task?**
- React components
- TypeScript interfaces
- MUI/Material-UI components
- State management (Redux/Context)
→ **Use Frontend Expert**

**Is this creating a specification?**
- Feature design
- Architecture diagrams
- Database schema design
- API contract definition
→ **Use Design Agent**

**Is this implementing from a spec?**
- Coding features per existing spec
- Multi-component implementation
- Integration work
→ **Use Coding Agent**

**Is this reviewing work?**
- Code review
- Documentation review
- Script compliance check
- Security audit
→ **Use Review Coordinator**

**Is this managing issues?**
- Creating GitHub issues
- Closing GitHub issues
- Updating issue status
- Issue triage
→ **Use Issue Manager**

**Is this running tests?**
- Test execution
- Coverage analysis
- Test failure investigation
→ **Use Testing Agent**

**Is this project management?**
- Sprint planning
- Milestone tracking
- Velocity analysis
→ **Use Project Manager**

### Step 2: If User Request is Ambiguous

**ALWAYS ask the user which agent to use when request is unclear.**

❌ **BAD** (Don't do this):
```
User: "Continue with development"
Claude: [Starts coding directly without knowing which agent to use]
```

❌ **BAD** (Don't do this):
```
User: "Go on with App Development Plan"
Claude: [Looks at next issue and starts implementing without asking]
```

✅ **GOOD** (Do this):
```
User: "Continue with development"
Claude: "I see the next task is Issue #4 (Create database schema).

This is a backend development task. According to CLAUDE.md, backend
development requires the Backend Expert agent for Python/FastAPI/SQLAlchemy
best practices.

Should I activate the Backend Expert agent to implement the database models?"
```

✅ **GOOD** (Do this):
```
User: "Go on with App Development Plan"
Claude: "Looking at the App Development Plan, the next task is Issue #4
(Database schema implementation).

Before proceeding, I need to clarify which agent to use:
A) Backend Expert - To implement SQLAlchemy models
B) Design Agent - To review/enhance the database spec first

According to CLAUDE.md mandatory rules, backend development should use
Backend Expert. Shall I activate that agent now?"
```

### Step 3: Check Mandatory Agent Requirements

**These tasks REQUIRE specific agents (NO EXCEPTIONS):**

| Task | Required Agent | Why Mandatory |
|------|----------------|---------------|
| Close ANY issue | Issue Manager | Ensures verification comment, CHANGELOG update, proper workflow |
| Modify CLAUDE.md | Review Coordinator | Prevents contradictions, ensures consistency, quality control |
| Modify scripts/ | Review Coordinator | Ensures folder structure, README compliance, category updates |
| Backend development | Backend Expert | Python/FastAPI/SQLAlchemy best practices, async patterns |
| Frontend development | Frontend Expert | React/TypeScript/MUI architecture, state management |
| Create feature specs | Design Agent | Ensures implementation-ready specs with API contracts |
| Code review | Review Coordinator | Quality, security, spec compliance, test coverage |
| Test execution | Testing Agent | Proper test setup, coverage analysis, failure reporting |

**Violation Consequences**:
- ❌ Implementing backend code without Backend Expert → Likely missing best practices
- ❌ Closing issue without Issue Manager → Missing verification, CHANGELOG not updated
- ❌ Modifying CLAUDE.md without Review Coordinator → Risk of contradictions, broken rules

### Step 4: If No Agent Matches

**For trivial tasks**, you can proceed directly:
- Updating simple README content
- Creating .gitkeep files
- Fixing typos in comments
- Simple git operations (pull, status)

**But if in doubt, ALWAYS ASK THE USER.**

---

## Enforcement Checklist

**At the start of EVERY task, complete this checklist:**

- [ ] **Did I identify the task type?** (backend, frontend, design, review, etc.)
- [ ] **Did I check if it requires a mandatory agent?** (See Step 3 table)
- [ ] **If ambiguous, did I ask the user which agent to use?**
- [ ] **Am I using the correct agent for this task?**
- [ ] **If trivial task, did I confirm it doesn't need an agent?**

**If ANY checkbox is NO → STOP and ask the user.**

### Quick Decision Tree

```
New task arrives
    ↓
Is it trivial (typo fix, .gitkeep)?
    YES → Proceed directly
    NO → Continue
         ↓
Is task type clear (backend/frontend/review/etc)?
    YES → Check mandatory agent table (Step 3)
    NO → ASK USER which agent to use
         ↓
Is there a mandatory agent for this task?
    YES → Activate that agent
    NO → Proceed with general capabilities
         ↓
Confirm with user if still unsure
```

---

## Permanent Agent System

**ETEx uses specialized permanent agents for consistent workflows.**

### Agent Overview

| Agent | Purpose | When Mandatory | CLAUDE.md Location |
|-------|---------|----------------|-------------------|
| **Issue Manager** | Create/update/close GitHub issues | Closing ANY issue | [.agents/issue-manager/CLAUDE.md](.agents/issue-manager/CLAUDE.md) |
| **Review Coordinator** | Review docs/code/scripts for compliance | Before committing to CLAUDE.md or scripts/ | [.agents/review-coordinator/CLAUDE.md](.agents/review-coordinator/CLAUDE.md) |
| **Design** | Create feature specifications | Complex features (>1 week) | [.agents/design/CLAUDE.md](.agents/design/CLAUDE.md) |
| **Coding** | Implement features per spec | Multi-component features | [.agents/coding/CLAUDE.md](.agents/coding/CLAUDE.md) |
| **Testing** | Run tests, report failures | Before PR, recommended | [.agents/testing/CLAUDE.md](.agents/testing/CLAUDE.md) |
| **Backend Expert** | Python/FastAPI/SQLAlchemy best practices | Backend features, DB migrations | [.agents/backend-expert/CLAUDE.md](.agents/backend-expert/CLAUDE.md) |
| **Frontend Expert** | React/TypeScript/MUI architecture | Complex UI components, state management | [.agents/frontend-expert/CLAUDE.md](.agents/frontend-expert/CLAUDE.md) |
| **Project Manager** | Sprint planning, milestone tracking | Weekly reviews, sprint planning | [.agents/project-manager/CLAUDE.md](.agents/project-manager/CLAUDE.md) |

### Folder Structure

```
.agents/
├── README.md                    # Agent system overview
├── workspace/                   # Shared temporary files (gitignored)
├── outputs/                     # Shared outputs (committed)
├── issue-manager/
│   └── CLAUDE.md                # Issue Manager instructions
├── review-coordinator/
│   └── CLAUDE.md                # Review Coordinator instructions
├── design/
│   └── CLAUDE.md                # Design Agent instructions
├── coding/
│   └── CLAUDE.md                # Coding Agent instructions
├── testing/
│   └── CLAUDE.md                # Testing Agent instructions
├── backend-expert/
│   └── CLAUDE.md                # Backend Expert instructions
├── frontend-expert/
│   └── CLAUDE.md                # Frontend Expert instructions
└── project-manager/
    └── CLAUDE.md                # Project Manager instructions
```

### How to Activate Agents

**Method 1: Explicit invocation**
```
User: "Act as Issue Manager - close issue #23"
User: "Switch to Review Coordinator - review CLAUDE.md changes"
User: "As Design Agent, create spec for PDF upload"
```

**Method 2: Automatic detection**
- User mentions "close issue" → Issue Manager activates
- File in scripts/ changed → Review Coordinator activates
- User says "create spec" → Design Agent activates

### Mandatory Agent Usage

**You MUST use these agents for**:

1. **Closing ANY GitHub issue** → Issue Manager
   - Ensures verification comment
   - Ensures CHANGELOG updated
   - Ensures proper closure documentation

2. **Modifying CLAUDE.md** → Review Coordinator
   - Checks for contradictions
   - Verifies formatting
   - Ensures rules are actionable

3. **Modifying scripts/** → Review Coordinator
   - Verifies subfolder + README structure
   - Checks script header compliance
   - Ensures category README updated

4. **Implementing complex features** → Design Agent first
   - Creates specification
   - Defines API contracts
   - Specifies testing strategy

### Agent Communication

**Agents communicate via**:
1. **GitHub Issues** - Issue Manager creates, others work on them
2. **Workspace files** - `.agents/workspace/<agent>/` for handoffs
3. **Output files** - `.agents/outputs/<agent>/` for final deliverables

**Example workflow**:
```
Review Coordinator finds problem
  → Requests issue via Issue Manager
  → Issue Manager creates issue #45
  → Design Agent creates spec (if needed)
  → Coding Agent implements
  → Testing Agent verifies
  → Issue Manager closes with verification
```

**See**: [.agents/README.md](.agents/README.md) for complete agent system documentation

---

## [Design Role] - When Designing Features

**For complete Design Agent instructions, workflows, and examples, see: [.agents/design/CLAUDE.md](.agents/design/CLAUDE.md)**

### Quick Summary
- **Purpose**: Create implementation-ready feature specifications
- **Key Outputs**: Database schemas, API contracts, architecture diagrams, ADRs
- **Workspace**: `.agents/workspace/design/` (drafts) → `docs/architecture/` (final specs)
- **When to Use**: Complex features (>1 week), architectural changes, new integrations

---

## [Coding Role] - When Implementing Features

**For complete Coding Agent instructions, workflows, and examples, see: [.agents/coding/CLAUDE.md](.agents/coding/CLAUDE.md)**

### Quick Summary
- **Purpose**: Implement features per specification with tests
- **Key Outputs**: Production code in `src/`, tests in `tests/`, 80%+ coverage
- **Code Reuse**: Import from `vendor/glossary-app/` (Tier 1) or copy with attribution (Tier 2)
- **When to Use**: After design spec is complete and approved

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

**For complete Review Coordinator instructions, workflows, and examples, see: [.agents/review-coordinator/CLAUDE.md](.agents/review-coordinator/CLAUDE.md)**

### Quick Summary
- **Purpose**: Review code for functionality, quality, security, and spec compliance
- **Key Outputs**: Approval documents or detailed fix lists with severity levels
- **Review Areas**: Functionality, code quality, security (XSS/SQL injection), performance, testing (80%+ coverage)
- **When to Use**: After implementation complete, before merging to main branch

---

## Multi-Agent Mode (3 Parallel Instances)

**If running 3 Claude Code instances simultaneously**:

### Agent Workspaces

Each agent works in their own workspace to avoid conflicts:

```
.agents/workspace/
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
1. Review agent: Create fix list in `.agents/outputs/review/fixes/`
2. Review agent: Update GitHub Issue: "Needs Fixes - see review report"
3. Coding agent: Read fix list, apply fixes, re-submit

### Conflict Prevention

**File Ownership Rules**:
- Design agent: OWNS `docs/architecture/`, `docs/adr/`, `.agents/workspace/design/`
- Coding agent: OWNS `src/`, `tests/`, `.agents/workspace/coding/`
- Review agent: OWNS `.agents/workspace/review/`, `.agents/outputs/review/`
- All agents: CAN READ everything, but respect ownership for writes

**Progress Communication**:
- Use git commits (automatic timestamps, clear history)
- Use GitHub Issues/Project boards (visual tracking)
- Don't rely on shared status files (merge conflicts)

---

## Common Tasks

### GitHub Workflow - Projects & Issue Tracking

**ETEx uses GitHub Projects v2 for 6-week MVP sprint tracking.**

#### Project Structure

- **Project Board**: "ETEx MVP - 6 Week Sprint" (Kanban + Roadmap views)
- **Iterations**: 6 sprints × 1 week (Week 1, Week 2, ..., Week 6)
- **Milestone**: "v1.0 MVP" for overall completion tracking
- **Labels**: 22 labels (9 essential + 13 agent-specific)

#### Board Columns

Simple 3-column Kanban:
- **To Do** - Ready for work, not started
- **In Progress** - Actively being worked on
- **Done** - Completed and closed

#### Views

- **Board View**: Daily Kanban (filtered to current sprint)
- **Table View**: Full issue list for sprint planning and filtering
- **Roadmap View**: Timeline showing 6-week overview with sprint markers

#### Issue Lifecycle

**Standard workflow**:

1. **Create**: Issue created → assigned to Week N → status "To Do"
   ```bash
   gh issue create --title "feat(backend): PDF upload API" \
     --label "type:feature,priority:high,component:backend" \
     --milestone "Week 2" \
     --body "See docs/architecture/feature-pdf-upload-spec.md"
   ```

2. **Start**: Agent starts work → move to "In Progress"
   ```bash
   # Update Project board manually or via automation
   # Begin implementation
   git commit -m "feat(backend): Start PDF upload implementation
   Relates to #15"
   ```

3. **Complete**: Create PR with "Closes #N" in description
   ```bash
   gh pr create --title "feat(backend): PDF upload API" \
     --body "Implements PDF upload with validation

   Closes #15"
   ```

4. **Merge**: PR merges → issue auto-closes → moves to "Done"

5. **Verify**: Add summary comment with verification checklist
   ```bash
   gh issue comment 15 --body "✅ Closed via PR #42

   **Verification**:
   - ✅ All tests pass (coverage: 85%)
   - ✅ CHANGELOG.md updated
   - ✅ Manual testing successful

   Issue fully resolved."
   ```

#### Issue Closing Requirements (MANDATORY)

**Before closing any issue, ensure**:

- ✅ **Summary comment** explaining what was done
- ✅ **Link to PR** that implemented the fix
- ✅ **All tests passing** (run test suite)
- ✅ **CHANGELOG.md updated** (if user-facing change)
- ✅ **Documentation updated** (if API/feature change)

**Auto-close (preferred)**:
```bash
# In PR description or commit message:
Closes #15
Fixes #23

# When PR merges → issues auto-close
```

**Manual close scenarios**:
- Duplicate issue → `gh issue close 15 --reason "duplicate"` + link to original
- Won't fix/out of scope → `gh issue close 15 --reason "not planned"` + explanation
- Resolved without PR → `gh issue close 15 --reason "completed"` + summary

#### Issue Rules

- ✅ Issues represent **1-2 weeks max** work (split larger issues)
- ✅ Issues shouldn't stay open > 1-2 months (review stale issues)
- ✅ Use `Relates to #N` in commits during work
- ✅ Use `Closes #N` or `Fixes #N` in PR for auto-close
- ✅ Always add verification comment when closing

#### Project Board Usage

**Daily**:
- Check "In Progress" column
- Move completed items to "Done"
- Update issue comments with progress

**Weekly**:
- Review milestone progress: `gh issue list --milestone "Week 2"`
- Check Timeline view for workload balance
- Create issues for next week
- Review and close stale issues

**Sprint Planning** (start of each week):
- Move issues from "To Do" to "In Progress" for current sprint
- Assign issues to agents
- Verify all issues have proper labels and milestones

#### Example: Complete Issue Lifecycle

```bash
# Week 2, Monday - Create issue
gh issue create \
  --title "feat(backend): PDF upload API" \
  --label "type:feature,priority:high,component:backend,phase:mvp" \
  --milestone "Week 2" \
  --body "Implement /api/documents/upload per spec"
# Issue #15 created → "To Do" column

# Week 2, Tuesday - Start work
# Move #15 to "In Progress" on Project board
git commit -m "feat(backend): Add PDF upload endpoint skeleton
Relates to #15"

# Week 2, Wednesday - Complete implementation
git commit -m "feat(backend): Complete PDF upload with validation
- File type validation (PDF only)
- 10MB size limit
- Tests: 85% coverage
Relates to #15"

# Week 2, Thursday - Create PR
gh pr create --title "feat(backend): PDF upload API" \
  --body "Implements PDF upload with validation

**Changes**:
- /api/documents/upload endpoint
- File validation (type, size)
- Error handling
- Tests: 85% coverage

Closes #15"

# Week 2, Friday - PR merged
gh pr merge 42 --squash
# Issue #15 auto-closes → "Done" column

# Add verification comment
gh issue comment 15 --body "✅ Closed via PR #42

**Verification**:
- ✅ Tests pass (coverage: 85%)
- ✅ CHANGELOG.md updated
- ✅ Tested with 5MB PDF: Success
- ✅ Tested with 15MB PDF: Rejected correctly

Issue fully resolved."
```

**See**: [docs/reference/github-project-setup.md](docs/reference/github-project-setup.md) for detailed setup guide

---

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

## MCP Server Integration

**Model Context Protocol (MCP) servers extend Claude Code's capabilities with specialized tools.**

### Essential MCP Servers for ETEx

**Priority 1 - Install Before Week 1**:

1. **GitHub MCP** ⭐ CRITICAL
   - Manage issues, PRs, milestones without leaving Claude Code
   - Essential for Issue Manager and Project Manager agents
   - Installation: `claude mcp add --transport http github https://api.githubcopilot.com/mcp/`
   - Requires: GitHub Personal Access Token (scopes: repo, workflow)

2. **Sequential Thinking MCP** ⭐ CRITICAL
   - Enables structured problem-solving for complex tasks
   - Critical for Design Agent (architecture decisions)
   - Installation: `claude mcp add sequential-thinking npx -- -y @modelcontextprotocol/server-sequential-thinking`
   - Usage: Add "use sequential thinking" to prompts

3. **Knowledge Graph Memory MCP** ⭐ CRITICAL
   - Retains ETEx context across sessions
   - Remembers agent roles, code reuse decisions, project structure
   - Prevents repetitive explanations
   - Installation: See [docs/reference/mcp-server-integration.md](docs/reference/mcp-server-integration.md)

**Priority 2 - Install Week 1-2**:

4. **Context7 MCP** (Latest library documentation)
   - Current FastAPI, SQLAlchemy 2.0, React 18, MUI docs
   - Usage: Add "use context7" to prompts
   - Free tier: 100 requests/day

5. **DuckDuckGo MCP** (Web search for solutions)
   - Search for error solutions, examples, current docs
   - No API key required
   - Good for Backend/Frontend Expert agents

**Priority 3 - Optional**:

6. **Playwright MCP** (E2E testing) - Week 5-6
7. **Apidog MCP** (API spec validation) - Week 3+
8. **MCP Compass** (Discover new MCP servers)

### Usage Patterns by Agent

**Issue Manager**:
```
"Create Week 2 issue for PDF upload with labels type:feature,priority:high"
```

**Design Agent**:
```
"Use sequential thinking to design database schema"
```

**Backend Expert**:
```
"Show latest SQLAlchemy 2.0 async patterns using context7"
```

**Frontend Expert**:
```
"Generate React component with MUI v5 using context7"
```

**Project Manager**:
```
"Analyze Week 3 velocity using GitHub data"
```

**Complete Setup Guide**: See [docs/reference/mcp-server-integration.md](docs/reference/mcp-server-integration.md) for detailed installation instructions, configuration, and troubleshooting.

### Verification

After installing MCPs:
```bash
# List installed MCPs
claude mcp list

# Test GitHub MCP
claude mcp test github "List open issues"

# Test Sequential Thinking
claude mcp test sequential-thinking "Break down: Design database schema"
```

### Security

- ✅ Store API keys in `.claude/settings.local.json` (gitignored)
- ❌ Never commit API keys to repository
- ✅ Use environment variables for CI/CD
- ✅ Rotate GitHub PATs every 90 days

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
- Post question in `.agents/workspace/coding/questions.md` if multi-agent mode

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
**Last Updated**: 2025-11-01
**Version**: 1.1 (Added CRITICAL: Pre-Task Agent Check section)
