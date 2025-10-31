# Create Agent Labels Script

**Purpose**: Create 13 agent-specific GitHub labels for ETEx repository
**Category**: Development Helper Script
**Last Updated**: 2025-10-31

---

## Overview

This script creates specialized labels for Claude Code agents (Design, Coding, Review, Explore) to categorize issues they create during development.

**Labels Created**: 13 total

- **Agent Roles** (4): `agent: design`, `agent: coding`, `agent: review`, `agent: explore`
- **Finding Types** (5): `type: design-issue`, `type: clarification`, `type: question`, `type: observation`, `type: blocked`
- **Severity Levels** (4): `severity: critical`, `severity: major`, `severity: minor`, `severity: suggestion`

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
cd scripts\dev\github\create-agent-labels

# Run script
.\create-agent-labels.ps1
```

### Output Example

```
Creating 13 agent labels...
  agent: design... Created
  agent: coding... Created
  agent: review... Created
  agent: explore... Created
  type: design-issue... Created
  type: clarification... Created
  type: question... Created
  type: observation... Created
  type: blocked... Created
  severity: critical... Created
  severity: major... Created
  severity: minor... Created
  severity: suggestion... Created

Summary: 13 created, 0 skipped
View at: https://github.com/developer-hhiotsystems/ETEx/labels
```

---

## Label Details

### Agent Role Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `agent: design` | Purple `#9C27B0` | Issue created by Design Agent (spec ambiguities, architecture questions) |
| `agent: coding` | Blue `#2196F3` | Issue created by Coding Agent (implementation blockers, technical questions) |
| `agent: review` | Orange `#FF9800` | Issue created by Review Agent (code quality, security findings) |
| `agent: explore` | Green `#4CAF50` | Issue created by Explore Agent (codebase insights, pattern observations) |

### Finding Type Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `type: design-issue` | Pink `#E91E63` | Specification ambiguity or gap requiring clarification |
| `type: clarification` | Amber `#FFC107` | Needs user decision or input |
| `type: question` | Cyan `#00BCD4` | Question about codebase or requirements |
| `type: observation` | Grey `#9E9E9E` | Interesting finding worth noting |
| `type: blocked` | Red `#D73A4A` | Cannot proceed without user action |

### Severity Level Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `severity: critical` | Dark Red `#B60205` | Must fix immediately (security, broken functionality) |
| `severity: major` | Red `#D93F0B` | Should fix before merge (quality issues, performance) |
| `severity: minor` | Yellow `#FBCA04` | Nice to fix (code style, minor optimizations) |
| `severity: suggestion` | Green `#0E8A16` | Optional improvement (best practices, enhancements) |

---

## When Agents Use These Labels

**Design Agent** finding spec ambiguity:
```bash
gh issue create \
  --title "clarification: IATE API auth method unclear [agent-generated]" \
  --label "agent: design,type: clarification,priority: high"
```

**Review Agent** finding security issue:
```bash
gh issue create \
  --title "bug(backend): SQL injection in search [agent-generated]" \
  --label "agent: review,type: bug,severity: critical,priority: critical"
```

**Coding Agent** blocked:
```bash
gh issue create \
  --title "blocked: Missing spaCy German model [agent-generated]" \
  --label "agent: coding,type: blocked,priority: high"
```

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

### Problem: Labels already exist

**Behavior**: Script will skip existing labels gracefully

```
Creating 13 agent labels...
  agent: design... Exists
  agent: coding... Created
  ...
Summary: 1 created, 12 skipped
```

**This is normal** - not an error! Script is idempotent.

---

## Related Documentation

- **Complete label system**: [scripts/dev/github/README.md](../README.md)
- **Agent issue guidelines**: [CLAUDE.md](../../../../CLAUDE.md) - "Agent-Generated Issues" section
- **GitHub workflow guide**: [docs/reference/github-workflow-guide.md](../../../../docs/reference/github-workflow-guide.md)

---

**For issues or improvements**: Create GitHub issue with label `type: meta`
