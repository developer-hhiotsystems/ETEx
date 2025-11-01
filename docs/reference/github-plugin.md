# GitHub Admin Plugin - Integration Guide

**Last Updated**: 2025-11-01
**Plugin Version**: v1.0.0
**Repository**: https://github.com/developer-hhiotsystems/claude-github-setup-plugin (private)
**Integration Status**: ✅ **ADOPTED** (Python library only, NOT CLI)

---

## Overview

The **claude-github-setup-plugin** provides a Python library for GitHub issue management operations. This guide covers installation, usage, and integration with ETEx workflows.

### Integration Decision

**RECOMMENDATION**: Use Python library as **fallback** to GitHub MCP

- ✅ **Primary**: GitHub MCP (via Claude Code)
- ✅ **Fallback**: GitHub Admin Plugin Python library
- ❌ **NOT RECOMMENDED**: Plugin CLI (Windows Unicode compatibility issues)

**See**: [.agents/outputs/review-coordinator/github-plugin-integration-report.md](../../.agents/outputs/review-coordinator/github-plugin-integration-report.md) for detailed analysis.

---

## Installation

### Prerequisites

- Python 3.12+ (ETEx venv)
- GitHub CLI (`gh`) installed and authenticated
- GitHub Personal Access Token with required scopes (see [Authentication](#authentication))

### Install Plugin

```bash
# From ETEx project root
C:\Users\developer\Documents\Coding Projects\ETEx\venv\Scripts\python.exe -m pip install git+https://github.com/developer-hhiotsystems/claude-github-setup-plugin.git
```

**Note**: Installation uses GitHub authentication, so you must be authenticated with `gh` CLI first.

### Verify Installation

```bash
# Check CLI is available (though we won't use it due to Unicode issues)
C:\Users\developer\Documents\Coding Projects\ETEx\venv\Scripts\gh-admin.exe --help

# Test Python library
python -c "from github.issues import IssueManager; print('✅ Plugin installed successfully')"
```

---

## Authentication

### Required Token Scopes

The plugin requires a GitHub Personal Access Token with these scopes:

- ✅ **`repo`** (full control) - For issue, PR, and repository operations
- ✅ **`workflow`** - For GitHub Actions integration
- ✅ **`project`** - For Project board management
- ✅ **`read:org`** - For organization-level operations (if needed)

### Setup Authentication

The plugin uses GitHub CLI for authentication:

```bash
# Check current authentication status
gh auth status

# If not authenticated or token expired, login again
gh auth login

# Refresh token with required scopes
gh auth refresh -s repo -s workflow -s project -s read:org
```

**Verify authentication**:
```bash
gh api user
# Should return your GitHub user data
```

### Authentication Methods

Plugin supports two authentication methods (in order of precedence):

1. **GitHub CLI keyring** (preferred)
   - Stored securely in system keyring
   - Automatically refreshed by `gh` CLI

2. **`GITHUB_TOKEN` environment variable** (CI/CD)
   - Set in `.claude/settings.local.json` or environment
   - Useful for automation and CI/CD pipelines

---

## Python Library Usage

### Basic Example

```python
from github.issues import IssueManager

# Auto-detect repository from git remote (recommended)
im = IssueManager()

# Or specify explicitly
im = IssueManager(repo="developer-hhiotsystems/ETEx")

# Create an issue
issue = im.create(
    title="feat(backend): Add IATE API caching",
    labels=["type:feature", "priority:medium", "phase:mvp", "component:backend"],
    milestone="Week 4",
    body="""Implement caching for IATE API to reduce request volume.

**Acceptance Criteria**:
- Redis-based caching with 24h TTL
- Cache hit rate > 80%
- Fallback to direct API on cache miss

**See**: docs/architecture/feature-iate-caching-spec.md"""
)

print(f"Created issue #{issue['number']}: {issue['html_url']}")
```

### Issue Operations

#### Create Issue

```python
from github.issues import IssueManager

im = IssueManager()

issue = im.create(
    title="feat(backend): Feature name",
    body="Description with acceptance criteria",
    labels=["type:feature", "priority:high", "phase:mvp", "component:backend"],
    milestone="Week 2",
    assignees=["developer-hhiotsystems"]  # Optional
)
```

#### Close Issue with Verification Comment

```python
im = IssueManager()

# Close with verification comment
im.close(
    issue_number=15,
    comment="""✅ Closed via PR #42

**Verification**:
- ✅ All tests pass (coverage: 85%)
- ✅ CHANGELOG.md updated
- ✅ Manual testing successful

Issue fully resolved."""
)
```

#### Add Comment

```python
im = IssueManager()

im.comment(
    issue_number=15,
    body="""Implementation 60% complete.

**Progress**:
- ✅ API endpoint created
- ✅ File validation implemented
- ⏳ Tests in progress (current)

ETA: End of week"""
)
```

#### Update Issue

```python
im = IssueManager()

# Update labels
im.edit(
    issue_number=15,
    labels=["type:feature", "priority:critical", "phase:mvp", "component:backend"]
)

# Update title and body
im.edit(
    issue_number=15,
    title="feat(backend): Updated title",
    body="Updated description"
)
```

#### List Issues

```python
im = IssueManager()

# List all open issues
issues = im.list(state="open")

# Filter by labels and milestone
issues = im.list(
    state="open",
    labels=["type:bug", "priority:high"],
    milestone="Week 2"
)

for issue in issues:
    print(f"#{issue['number']}: {issue['title']}")
```

#### View Issue Details

```python
im = IssueManager()

issue = im.view(issue_number=15)
print(f"Title: {issue['title']}")
print(f"State: {issue['state']}")
print(f"Labels: {[label['name'] for label in issue['labels']]}")
```

#### Reopen Issue

```python
im = IssueManager()

im.reopen(issue_number=15)
```

### Label Operations

```python
from github.labels import LabelManager

lm = LabelManager()

# Create custom label
lm.create(
    name="custom-label",
    color="ff0000",
    description="My custom label"
)

# Create standard label scheme
lm.create_standard_scheme()

# List all labels
labels = lm.list()
```

### Milestone Operations

```python
from github.milestones import MilestoneManager

mm = MilestoneManager()

# Create milestone
mm.create(
    title="Week 5",
    due_date="2025-02-15",
    description="Week 5 sprint tasks"
)

# List milestones
milestones = mm.list(state="open")

# Close milestone
mm.close(milestone_number=1)
```

---

## ETEx Integration Patterns

### Pattern 1: ETEx-Specific Issue Creation

```python
"""
ETEx-specific issue creation with validation.
Location: .agents/issue-manager/utils.py
"""

from github.issues import IssueManager

def create_etex_issue(title, labels, milestone, body):
    """Create issue with ETEx label validation."""
    # Validate required label categories
    required_prefixes = {"type:", "priority:", "phase:"}
    label_prefixes = {label.split(":")[0] + ":" for label in labels if ":" in label}

    missing = required_prefixes - label_prefixes
    if missing:
        raise ValueError(f"Missing required label categories: {missing}")

    # Create issue
    im = IssueManager()
    return im.create(title, body, labels, milestone)
```

### Pattern 2: Verified Issue Closure

```python
"""
Close issue with full ETEx verification workflow.
Location: .agents/issue-manager/utils.py
"""

from github.issues import IssueManager
import subprocess

def close_issue_verified(issue_number, pr_number):
    """Close issue after verifying PR, tests, and CHANGELOG."""

    # 1. Verify PR merged
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_number), "--json", "mergedAt", "-q", ".mergedAt"],
        capture_output=True,
        text=True
    )
    if not result.stdout.strip():
        raise ValueError(f"PR #{pr_number} not merged yet")

    # 2. Run tests
    test_result = subprocess.run(
        ["pytest", "tests/", "--cov", "--cov-report=term-missing"],
        capture_output=True,
        text=True
    )
    if test_result.returncode != 0:
        raise ValueError("Tests failing - cannot close issue")

    # Extract coverage
    import re
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", test_result.stdout)
    coverage = match.group(1) if match else "N/A"

    # 3. Check CHANGELOG
    try:
        with open("CHANGELOG.md", "r") as f:
            changelog_content = f.read()
            changelog_updated = f"#{pr_number}" in changelog_content or f"PR #{pr_number}" in changelog_content
    except FileNotFoundError:
        changelog_updated = False

    # 4. Build verification comment
    comment = f"""✅ Closed via PR #{pr_number}

**Verification**:
- ✅ PR merged
- ✅ All tests pass (coverage: {coverage}%)
- {'✅' if changelog_updated else '⚠️ '} CHANGELOG.md updated
{'' if changelog_updated else '  **Note**: CHANGELOG may need manual verification'}

Issue fully resolved and verified."""

    # 5. Close issue with verification
    im = IssueManager()
    return im.close(issue_number, comment=comment)
```

### Pattern 3: Hybrid GitHub MCP + Plugin

```python
"""
Use GitHub MCP as primary, plugin as fallback.
Location: .agents/issue-manager/utils.py
"""

from github.issues import IssueManager

def create_issue_hybrid(title, labels, milestone, body):
    """Create issue using best available method."""
    try:
        # Try GitHub MCP first (if available in Claude Code)
        return mcp__github__create_issue(
            owner="developer-hhiotsystems",
            repo="ETEx",
            title=title,
            labels=labels,
            milestone=milestone,
            body=body
        )
    except (NameError, Exception):
        # Fall back to plugin
        im = IssueManager()
        return im.create(title, body, labels, milestone)
```

---

## Limitations and Workarounds

### Known Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **CLI has Unicode issues** | CLI unusable on Windows | Use Python library only |
| **No CHANGELOG integration** | Manual CHANGELOG updates required | Implement in wrapper function |
| **No PR operations** | Cannot verify PR status | Use GitHub MCP or `gh pr` CLI |
| **No test execution** | Cannot run tests | Use Testing Agent |
| **Requires `gh` CLI** | Dependency on external tool | Document setup clearly |

### Critical Gap: CHANGELOG Updates

**Problem**: Plugin does NOT automatically update CHANGELOG.md when closing issues.

**Solution**: Implement manual verification in `close_issue_verified()` wrapper:

```python
# In .agents/issue-manager/utils.py
def check_changelog_updated(pr_number):
    """Check if CHANGELOG.md mentions the PR."""
    try:
        with open("CHANGELOG.md", "r") as f:
            content = f.read()
            return f"#{pr_number}" in content or f"PR #{pr_number}" in content
    except FileNotFoundError:
        return False

# Use in close workflow
if not check_changelog_updated(pr_number):
    print("⚠️  WARNING: CHANGELOG.md may not be updated - manual check required")
```

---

## Troubleshooting

### Issue: "Not authenticated"

**Symptoms**:
```
Error: Not authenticated with GitHub
```

**Solution**:
```bash
# Re-authenticate
gh auth login

# Verify
gh auth status
```

### Issue: "Permission denied"

**Symptoms**:
```
Error: Resource not accessible by integration
```

**Solution**:
```bash
# Check token scopes
gh auth status

# Refresh with required scopes
gh auth refresh -s repo -s workflow -s project -s read:org
```

### Issue: "Repository not found"

**Symptoms**:
```
Error: Could not resolve to a Repository
```

**Solution**:
```python
# Specify repo explicitly
im = IssueManager(repo="developer-hhiotsystems/ETEx")

# Or check git remote
# Ensure you're in ETEx directory with valid .git/ folder
```

### Issue: Unicode errors (CLI only)

**Symptoms**:
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
```

**Solution**:
```python
# Don't use CLI - use Python library instead
from github.issues import IssueManager
im = IssueManager()
# ... use Python API ...
```

### Issue: Token expired

**Symptoms**:
```
Error: Bad credentials
```

**Solution**:
```bash
# Refresh token
gh auth refresh -s repo -s workflow -s project

# Or create new token and update settings
# See: docs/reference/github-plugin.md#authentication
```

---

## Security Best Practices

### Token Management

- ✅ **Store tokens securely**: Use `gh` CLI keyring or `.claude/settings.local.json` (gitignored)
- ✅ **Rotate regularly**: Every 90 days minimum
- ✅ **Use fine-grained tokens**: When available, limit to specific repositories
- ✅ **Minimum scopes**: Only enable required scopes
- ❌ **Never commit tokens**: Ensure `.gitignore` includes settings files

### Token Storage Locations

**DO**:
```json
// .claude/settings.local.json (gitignored)
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

**DON'T**:
```json
// .claude/settings.json (committed to git - WRONG!)
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  // ❌ NEVER DO THIS
  }
}
```

### Audit and Monitoring

1. **Review plugin code changes**: Before updating plugin version
2. **Monitor API rate limits**: Check GitHub API usage regularly
3. **Audit issue operations**: Review logs for unexpected operations
4. **Limit access**: Only install plugin in trusted environments

---

## References

- **Plugin Repository**: https://github.com/developer-hhiotsystems/claude-github-setup-plugin (private)
- **Integration Report**: [.agents/outputs/review-coordinator/github-plugin-integration-report.md](../../.agents/outputs/review-coordinator/github-plugin-integration-report.md)
- **Issue Manager**: [.agents/issue-manager/CLAUDE.md](../../.agents/issue-manager/CLAUDE.md)
- **Quick Integration Guide**: [github-repo-setup.md](../../github-repo-setup.md)
- **GitHub CLI**: https://cli.github.com/
- **GitHub API Scopes**: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps

---

**Last Updated**: 2025-11-01
**Maintainer**: ETEx Development Team
**Status**: Active
