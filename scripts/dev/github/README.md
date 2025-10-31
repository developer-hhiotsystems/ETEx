# GitHub Workflow Scripts

**Purpose**: Automate GitHub workflow setup (labels, issues, project boards)
**Category**: Development Helper Scripts
**Last Updated**: 2025-10-31

---

## Prerequisites

- **GitHub CLI (`gh`)** installed and authenticated
  - Install: `winget install GitHub.cli`
  - Auth: `gh auth login`
- **Repository access**: `developer-hhiotsystems/ETEx`
- **Permissions**: `repo` scope (for creating labels/issues)

---

## Available Scripts

**Each script has its own subfolder with dedicated README.md** for detailed usage instructions.

| Script | Description | Location |
|--------|-------------|----------|
| **create-agent-labels** | Create 13 agent-specific labels (agent roles, finding types, severity) | [create-agent-labels/](create-agent-labels/) |
| **create-github-labels** | Create full set of 29 labels (type, priority, phase, component, status) | [create-github-labels/](create-github-labels/) |

---

## Common Workflows

### Workflow 1: First-Time GitHub Setup

**Create essential labels** (do this once):

```powershell
# Navigate to create-agent-labels directory
cd scripts\dev\github\create-agent-labels

# Create labels
.\create-agent-labels.ps1
```

**Verify**:
- Go to: https://github.com/developer-hhiotsystems/ETEx/labels
- Should see 13 new agent labels

**For detailed usage**: See [create-agent-labels/README.md](create-agent-labels/README.md)

---

### Workflow 2: Create Week 1 Issues

**After labels are created**:

```powershell
# Create first issue manually
gh issue create --repo developer-hhiotsystems/ETEx \
  --title "feat(backend): Create database schema (Week 1)" \
  --label "type: feature,priority: high,phase: mvp,component: backend" \
  --body "See docs/REQUIREMENTS.md section 13"
```

**Or use templates**:
- Go to: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=feature_request.yml
- Fill in form with dropdowns

---

## Script Details

### create-agent-labels.ps1

**Purpose**: Create 13 agent-specific labels for Design/Coding/Review/Explore agents

**Labels Created**:

**Agent Roles** (4):
- `agent: design` - Created by Design Agent
- `agent: coding` - Created by Coding Agent
- `agent: review` - Created by Review Agent
- `agent: explore` - Created by Explore Agent

**Finding Types** (5):
- `type: design-issue` - Spec ambiguity or gap
- `type: clarification` - Needs user decision
- `type: question` - Question about codebase
- `type: observation` - Interesting finding
- `type: blocked` - Cannot proceed

**Severity Levels** (4):
- `severity: critical` - Must fix now
- `severity: major` - Should fix before merge
- `severity: minor` - Nice to fix
- `severity: suggestion` - Optional improvement

**Usage**:
```powershell
# Dry run (test without creating)
.\create-agent-labels.ps1 -DryRun

# Create labels
.\create-agent-labels.ps1

# Custom repository
.\create-agent-labels.ps1 -repo "user/other-repo"
```

**Parameters**:
- `-repo` : GitHub repository (default: `developer-hhiotsystems/ETEx`)
- `-DryRun` : Test mode, don't create labels

**Output**:
```
========================================
ETEx Agent Label Creation Script
========================================

[1/4] Checking GitHub CLI...
  ✓ GitHub CLI found

[2/4] Checking authentication...
  ✓ Authenticated to GitHub

[3/4] Repository: developer-hhiotsystems/ETEx

[4/4] Creating 13 agent labels...

  Creating: agent: design (#9C27B0)
    ✓ Created successfully
  ...

========================================
Summary
========================================
  ✓ Created:       13
  ⊙ Already exist: 0
  ✗ Errors:        0
  ─ Total:         13
```

---

### create-github-labels.ps1

**Purpose**: Create full label set (29 labels) including essential + agent labels

**Labels Created**:
- **Type labels** (7): feature, bug, docs, refactor, test, chore, meta
- **Priority labels** (4): critical, high, medium, low
- **Phase labels** (8): mvp, 2a-2f, future
- **Component labels** (5): backend, frontend, database, extraction, api-integration
- **Status labels** (5): planning, ready, in-progress, review, blocked

**Usage**:
```powershell
.\create-github-labels.ps1
```

**Note**: If you already created the 9 essential labels manually, this will skip them.

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

### Problem: `could not add label: 'type: feature' not found`

**Cause**: Labels don't exist yet in repository

**Solution**:
```powershell
# Create labels first
.\create-agent-labels.ps1

# Then create issues
gh issue create --title "..." --label "type: feature,..."
```

---

### Problem: Labels already exist

**Behavior**: Script will skip existing labels gracefully
```
Creating: agent: design (#9C27B0)
  ⊙ Already exists (skipped)
```

**This is normal** - not an error!

---

## Integration with CLAUDE.md

**When agents create issues**, they should use these labels:

**Design Agent** finding spec ambiguity:
```powershell
gh issue create \
  --title "clarification: IATE API auth method unclear [agent-generated]" \
  --label "agent: design,type: clarification,priority: high"
```

**Review Agent** finding security issue:
```powershell
gh issue create \
  --title "bug(backend): SQL injection in search [agent-generated]" \
  --label "agent: review,type: bug,severity: critical,priority: critical"
```

**Coding Agent** blocked:
```powershell
gh issue create \
  --title "blocked: Missing spaCy German model [agent-generated]" \
  --label "agent: coding,type: blocked,priority: high"
```

See [CLAUDE.md](../../../CLAUDE.md) section "Agent-Generated Issues" for complete guidelines.

---

## Related Documentation

- **Workflow Guide**: [docs/reference/github-workflow-guide.md](../../../docs/reference/github-workflow-guide.md)
- **Issue Creation**: [docs/reference/create-week1-issues.md](../../../docs/reference/create-week1-issues.md)
- **Workflow Simulation**: [docs/reference/github-workflow-simulation.md](../../../docs/reference/github-workflow-simulation.md)
- **Scripts Organization**: [docs/reference/scripts-organization.md](../../../docs/reference/scripts-organization.md)

---

**For complete guidelines, see**: [Scripts Organization Guide](../../../docs/reference/scripts-organization.md)
