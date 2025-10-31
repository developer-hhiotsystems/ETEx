# .agent/ - Agent Workspace

**Purpose**: Temporary working space for Claude Code agents during feature development

---

## Folder Structure

```
.agent/
├── README.md           # This file
├── workspace/          # Temporary working files (gitignored)
│   ├── design/        # Design agent drafts
│   ├── coding/        # Coding agent working files
│   └── review/        # Review agent checklists
├── memory/            # Agent context/memory (gitignored)
└── outputs/           # Completed artifacts for review (committed)
    └── review/        # Review reports
```

---

## Usage

### Single Claude Instance (Primary Use Case)

When working alone with one Claude Code window:

```bash
# Use workspace/ for all temporary work
.agent/workspace/
├── feature-auth-draft.md      # Design work
├── implementation-notes.md    # Coding notes
└── review-checklist.md        # Review notes
```

### Multi-Agent Mode (3 Parallel Instances)

When running 3 Claude instances simultaneously, each uses their own subfolder:

```bash
.agent/workspace/
├── design/       # Design agent's workspace
├── coding/       # Coding agent's workspace
└── review/       # Review agent's workspace
```

---

## What Goes Where

### workspace/ (Gitignored)
**Purpose**: Temporary working files, drafts, notes

**Contents**:
- Draft specifications
- Implementation notes
- Debug logs
- Review checklists
- Scratch work

**Lifecycle**: Create → Work → Complete → Delete or archive

**Git**: Fully gitignored (never committed)

---

### memory/ (Gitignored)
**Purpose**: Agent memory and context files

**Contents**:
- Agent conversation context
- Session state
- Memory databases

**Git**: Fully gitignored

---

### outputs/ (Committed)
**Purpose**: Completed artifacts ready for human review

**Contents**:
- Review reports (`.agent/outputs/review/`)
- Fix lists (`.agent/outputs/review/fixes/`)
- Completed analysis documents

**Lifecycle**: Agent creates → Human reviews → Promote to docs/ or discard

**Git**: Committed (these are knowledge artifacts)

---

## Workflow Example

### Designing a Feature

```bash
# 1. Draft in workspace
vim .agent/workspace/design/feature-search-spec.md

# 2. Iterate and refine
# (multiple edits)

# 3. Finalize
mv .agent/workspace/design/feature-search-spec.md docs/architecture/

# 4. Commit
git add docs/architecture/feature-search-spec.md
git commit -m "docs: Add search feature specification"

# 5. Clean up workspace
rm -rf .agent/workspace/design/*
```

### Reviewing Code

```bash
# 1. Create review report in workspace
vim .agent/workspace/review/feature-auth-review.md

# 2. Run tests, check code

# 3. Complete review, move to outputs
mv .agent/workspace/review/feature-auth-review.md .agent/outputs/review/

# 4. Commit review report
git add .agent/outputs/review/feature-auth-review.md
git commit -m "review: Auth feature review complete"

# 5. If approved, promote docs to main docs/
# If fixes needed, create fix list in outputs/review/fixes/
```

---

## Maintenance

### Daily
- No action needed (workspace is temporary)

### Weekly
- Review `.agent/outputs/` - promote valuable content to `docs/` or delete

### Monthly
- Clean up old outputs: `rm -rf .agent/outputs/archive/`

---

## Git Strategy

```gitignore
# .gitignore

# Temporary working files (NOT committed)
.agent/workspace/
.agent/memory/

# Completed artifacts (committed for review)
!.agent/outputs/
```

**Why this strategy?**
- **workspace/**: Temporary, regenerate-able → gitignored
- **memory/**: Agent-specific context → gitignored
- **outputs/**: Knowledge artifacts → committed

---

## Questions & Answers

**Q: Can I work without this folder?**
A: Yes, for simple tasks. This structure is most valuable for complex features that span multiple sessions.

**Q: Should I clean workspace/ after every task?**
A: Not required, but recommended. Prevents clutter and confusion.

**Q: What if I have multiple tasks in progress?**
A: Create subfolders:
```
.agent/workspace/
├── task-001-search/
├── task-002-auth/
└── task-003-api/
```

**Q: Can I commit workspace files?**
A: Generally no (they're temporary). If something is valuable, move it to `docs/` or `.agent/outputs/` first, then commit.

---

**Last Updated**: 2025-10-31
