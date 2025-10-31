# Create GitHub Labels Script

**Purpose**: Create full set of 29 GitHub labels for ETEx repository organization
**Category**: Development Helper Script
**Last Updated**: 2025-10-31

---

## Overview

This script creates the complete label system for ETEx project management, including type, priority, phase, component, and status labels.

**Labels Created**: 29 total

- **Type** (7): feature, bug, docs, refactor, test, chore, meta
- **Priority** (4): critical, high, medium, low
- **Phase** (8): mvp, 2a-2f, future
- **Component** (5): backend, frontend, database, extraction, api-integration
- **Status** (5): planning, ready, in-progress, review, blocked

**Note**: This creates the "essential 9 labels" that were created manually, plus additional labels for full project tracking.

---

## Prerequisites

- **GitHub CLI (`gh`)** installed and authenticated
  - Install: `winget install GitHub.cli`
  - Auth: `gh auth login`
- **Repository access**: `developer-hhiotsystems/ETEx`
- **Permissions**: `repo` scope for creating labels

---

## Usage

### Basic Usage

```powershell
# Navigate to script directory
cd scripts\dev\github\create-github-labels

# Run script
.\create-github-labels.ps1
```

### Output Example

```
Creating GitHub labels for ETEx...

[Type Labels]
✓ label "type: feature" created
✓ label "type: bug" created
✓ label "type: docs" created
...

[Priority Labels]
✓ label "priority: critical" created
✓ label "priority: high" created
...

[Phase Labels]
✓ label "phase: mvp" created
...

[Component Labels]
✓ label "component: backend" created
...

[Status Labels]
✓ label "status: planning" created
...

All labels created successfully!
View at: https://github.com/developer-hhiotsystems/ETEx/labels
```

---

## Label Categories

### Type Labels (7)

| Label | Color | Description |
|-------|-------|-------------|
| `type: feature` | Green `#0E8A16` | New functionality |
| `type: bug` | Red `#D73A4A` | Something broken |
| `type: docs` | Blue `#0075CA` | Documentation only |
| `type: refactor` | Orange `#FFA500` | Code improvement |
| `type: test` | Yellow `#FBCA04` | Testing improvements |
| `type: chore` | Grey `#CCCCCC` | Maintenance tasks |
| `type: meta` | Purple `#5319E7` | Meta/tracking issues |

### Priority Labels (4)

| Label | Color | Description |
|-------|-------|-------------|
| `priority: critical` | Dark Red `#B60205` | Blocks MVP, security issue |
| `priority: high` | Red `#D93F0B` | Important for current week |
| `priority: medium` | Yellow `#FBCA04` | Normal priority |
| `priority: low` | Green `#0E8A16` | Nice to have |

### Phase Labels (8)

| Label | Color | Description |
|-------|-------|-------------|
| `phase: mvp` | Purple `#5319E7` | Must have for MVP (6 weeks) |
| `phase: 2a` | Light Blue `#C5DEF5` | Phase 2A (Internal docs) |
| `phase: 2b` | Light Blue `#C5DEF5` | Phase 2B (Deviation checking) |
| `phase: 2c` | Light Blue `#C5DEF5` | Phase 2C (DeepL integration) |
| `phase: 2d` | Light Blue `#C5DEF5` | Phase 2D (Additional languages) |
| `phase: 2e` | Light Blue `#C5DEF5` | Phase 2E (Synonym auto-detection) |
| `phase: 2f` | Light Blue `#C5DEF5` | Phase 2F (User accounts) |
| `phase: future` | Yellow `#E4E669` | Ideas for later |

### Component Labels (5)

| Label | Color | Description |
|-------|-------|-------------|
| `component: backend` | Blue `#1D76DB` | Python/FastAPI |
| `component: frontend` | Light Blue `#BFD4F2` | React/TypeScript |
| `component: database` | Teal `#006B75` | SQLite/Alembic |
| `component: extraction` | Purple `#7057FF` | PDF/term extraction |
| `component: api-integration` | Dark Teal `#008672` | IATE/IEC integration |

### Status Labels (5)

**Note**: These are optional - GitHub Projects board can manage status instead

| Label | Color | Description |
|-------|-------|-------------|
| `status: planning` | Light Purple `#D4C5F9` | Spec/design in progress |
| `status: ready` | Green `#0E8A16` | Ready for coding |
| `status: in-progress` | Yellow `#FBCA04` | Currently being worked on |
| `status: review` | Orange `#FFA500` | Code review needed |
| `status: blocked` | Red `#D73A4A` | Waiting on external dependency |

---

## Usage Examples

### Creating Issues with Labels

**Feature for MVP backend work**:
```bash
gh issue create \
  --title "feat(backend): Implement PDF upload API" \
  --label "type:feature,priority:high,phase:mvp,component:backend" \
  --milestone "Week 2"
```

**Bug in frontend (high priority)**:
```bash
gh issue create \
  --title "bug(frontend): Search results not displaying" \
  --label "type:bug,priority:high,component:frontend" \
  --milestone "Week 3"
```

**Documentation task**:
```bash
gh issue create \
  --title "docs: Add API endpoint documentation" \
  --label "type:docs,priority:medium,phase:mvp"
```

### Filtering Issues by Labels

```bash
# All MVP backend features
gh issue list --label "phase:mvp,component:backend,type:feature"

# All critical bugs
gh issue list --label "type:bug,priority:critical"

# All blocked issues
gh issue list --label "status:blocked"
```

---

## When to Use Which Labels

**Every issue should have**:
- 1 × Type label (what kind of work)
- 1 × Priority label (how urgent)
- 1 × Phase label (which release)
- 1+ × Component labels (which part of system)
- 0-1 × Status label (if not using Projects board)

**Example complete labeling**:
```
Issue: "feat(backend): Add IATE API caching"
Labels:
  type: feature
  priority: medium
  phase: mvp
  component: backend
  component: api-integration
```

---

## Relationship with Agent Labels

This script creates the **base label system**. For agent-specific labels (agent roles, finding types, severity), use:

```bash
# Navigate to agent labels script
cd ..\create-agent-labels

# Run agent labels script
.\create-agent-labels.ps1
```

**Complete label system** = This script (29 labels) + Agent labels script (13 labels) = **42 total labels**

---

## Troubleshooting

### Problem: `gh: command not found`

**Solution**:
```powershell
# Install GitHub CLI
winget install GitHub.cli

# Restart terminal
# Verify installation
gh --version
```

---

### Problem: `HTTP 403: Resource not accessible by personal access token`

**Cause**: GitHub token lacks `repo` permissions

**Solution**:
```powershell
# Re-authenticate with correct scopes
gh auth refresh -h github.com -s repo

# Or re-login completely
gh auth login
# Choose: GitHub.com → HTTPS → Browser → Grant repo access
```

---

### Problem: Some labels already exist

**Behavior**: Script will fail on existing labels

```
✓ label "type: feature" created
! label type:bug already exists
```

**Solution**: This is expected if you created the "9 essential labels" manually. The labels that already exist will show an error, but the script continues creating the rest.

---

### Problem: Want to update existing label colors

**Solution**:
```bash
# Edit existing label
gh label edit "type:feature" --color "00FF00" --description "New description"

# Or delete and recreate
gh label delete "type:feature"
.\create-github-labels.ps1
```

---

## Related Documentation

- **Agent-specific labels**: [scripts/dev/github/create-agent-labels/README.md](../create-agent-labels/README.md)
- **Complete GitHub workflow**: [docs/reference/github-workflow-guide.md](../../../../docs/reference/github-workflow-guide.md)
- **Label usage in CLAUDE.md**: [CLAUDE.md](../../../../CLAUDE.md) - "GitHub Workflow" section

---

**For issues or improvements**: Create GitHub issue with label `type: meta`
