# Quick Integration Guide

Copy this guide to any project to quickly integrate the GitHub Admin Plugin.

---

## Installation

```bash
# Install the plugin (works even though it's private - uses your gh auth)
pip install git+https://github.com/developer-hhiotsystems/claude-github-setup-plugin.git
```

**That's it!** The plugin is now available everywhere on your system.

---

## Usage - CLI Commands

### Quick Setup (New Project)

```bash
# Initialize your project with labels, milestones, and project board
gh-admin workflow setup-repo \
  --labels \
  --milestones "v0.1,v1.0,v2.0" \
  --project "Development Roadmap" \
  --repo owner/repo
```

### Common Commands

```bash
# Check authentication
gh-admin auth status

# Create an issue
gh-admin issue create "Bug: Login broken" \
  --label "type:bug,priority:high" \
  --milestone "v1.0" \
  --repo owner/repo

# List issues
gh-admin issue list --repo owner/repo

# Close an issue
gh-admin issue close 123 --repo owner/repo

# Create labels
gh-admin label create-scheme --repo owner/repo

# Create milestone
gh-admin milestone create "v1.0" \
  --due-date "2025-03-01" \
  --description "First release" \
  --repo owner/repo

# List milestones
gh-admin milestone list --repo owner/repo
```

**Tip:** Omit `--repo` if you run commands from within a git repository - it auto-detects!

---

## Usage - Python Library

### Quick Start

```python
#!/usr/bin/env python3
"""Example: Using GitHub Admin Plugin in your project."""

from github.issues import IssueManager
from github.labels import LabelManager
from github.milestones import MilestoneManager
from github.integrator import GitHubIntegrator

# Auto-detect repo from git remote, or specify explicitly
REPO = "owner/repo"  # or None to auto-detect

# Create an issue
im = IssueManager(repo=REPO)
issue = im.create(
    title="Implement user authentication",
    body="Add OAuth and JWT support",
    labels=["type:feature", "priority:high"],
    milestone="v1.0"
)
print(f"Created issue #{issue['number']}: {issue['url']}")

# Setup repository with standard configuration
gi = GitHubIntegrator(repo=REPO)
result = gi.setup_repository(
    create_labels=True,              # Create standard label scheme
    create_milestones=["v0.1", "v1.0", "v2.0"],
    create_project="Development Roadmap",
    owner="your-username"
)
print("Repository setup complete!")
```

### Common Operations

```python
from github.issues import IssueManager
from github.labels import LabelManager
from github.milestones import MilestoneManager

# Issues
im = IssueManager(repo="owner/repo")
im.create("Title", body="Description", labels=["bug"])
im.close(123, comment="Fixed!")
im.comment(123, "Update: Still working on this")
issues = im.list(state="open", labels=["bug"])

# Labels
lm = LabelManager(repo="owner/repo")
lm.create("custom-label", color="ff0000", description="My label")
lm.create_standard_scheme()  # Creates 10 standard labels
labels = lm.list()

# Milestones
mm = MilestoneManager(repo="owner/repo")
mm.create("v1.0", due_date="2025-03-01", description="First release")
mm.close(1)
milestones = mm.list(state="open")
```

### Automation Example

```python
#!/usr/bin/env python3
"""Automate project setup for new repository."""

from github.integrator import GitHubIntegrator

def setup_new_project(repo_name, owner):
    """Setup a new project with standard configuration."""

    gi = GitHubIntegrator(repo=repo_name)

    # Setup repository
    print(f"Setting up {repo_name}...")
    result = gi.setup_repository(
        create_labels=True,
        create_milestones=["Sprint 1", "Sprint 2", "v1.0"],
        create_project="Project Roadmap",
        owner=owner
    )

    # Create initial issues
    print("Creating initial issues...")
    gi.issues.create(
        title="Project setup complete",
        body="Repository initialized with labels, milestones, and project board",
        labels=["type:docs"],
        milestone="Sprint 1"
    )

    print(f"✓ Setup complete for {repo_name}")
    print(f"  Labels: {sum(1 for v in result['labels'].values() if v)}")
    print(f"  Milestones: {sum(1 for v in result['milestones'].values() if v)}")
    print(f"  Project: {'Created' if result.get('project') else 'Failed'}")

if __name__ == "__main__":
    setup_new_project("owner/my-new-project", "owner")
```

---

## Authentication

The plugin automatically uses your GitHub authentication:

```bash
# Check authentication
gh-admin auth status

# If not authenticated, login
gh auth login
```

**Token is stored securely in your system keyring** - no need to manage it manually!

---

## Repository-Specific Config (Optional)

Create `.github-admin.json` in your project root for defaults:

```json
{
  "repository": "owner/repo",
  "defaults": {
    "labels": ["bug", "feature", "docs"],
    "milestone": "v1.0",
    "project": "Main Roadmap"
  }
}
```

---

## Common Workflows

### Daily Development

```bash
# Create issue for new work
gh-admin issue create "Add search feature" \
  --label "type:feature" \
  --milestone "v1.0"

# Update issue status
gh-admin issue edit 42 --add-label "status:testing"

# Close when done
gh-admin issue close 42 --comment "Completed in PR #123"
```

### Sprint Planning

```bash
# Create sprint milestone
gh-admin milestone create "Sprint 5" --due-date "2025-02-15"

# Batch create issues
gh-admin issue create "Task 1" --milestone "Sprint 5"
gh-admin issue create "Task 2" --milestone "Sprint 5"
gh-admin issue create "Task 3" --milestone "Sprint 5"
```

### Project Board Management

```python
from github.projects import ProjectManager
from github.issues import IssueManager

pm = ProjectManager()
im = IssueManager(repo="owner/repo")

# Get project
projects = pm.list(owner="owner")
project_id = projects[0]['id']

# Add all open issues to project
issues = im.list(state="open")
for issue in issues:
    pm.add_item(project_id, issue['url'], owner="owner")
    print(f"Added issue #{issue['number']} to project")
```

---

## Tips

1. **Auto-detect repo**: Run commands from within git repo - no need for `--repo` flag
2. **Environment variable**: Set `GITHUB_REPO=owner/repo` to avoid repeating `--repo`
3. **Bash aliases**: Add shortcuts to `~/.bashrc`:
   ```bash
   alias ghi='gh-admin issue'
   alias ghl='gh-admin label'
   alias ghm='gh-admin milestone'
   ```
4. **Python scripts**: Import directly for automation
5. **CI/CD**: Works in GitHub Actions - token is automatic

---

## Help & Documentation

```bash
# CLI help
gh-admin --help
gh-admin issue --help
gh-admin label --help

# Full documentation
# Check: https://github.com/developer-hhiotsystems/claude-github-setup-plugin/docs/
```

---

## Troubleshooting

### "Not authenticated"
```bash
gh auth login
gh-admin auth status
```

### "Permission denied"
```bash
# Check token scopes
gh-admin auth validate

# Refresh with needed scopes
gh auth refresh -s repo -s project
```

### "Repository not found"
```bash
# Specify repo explicitly
gh-admin issue list --repo owner/repo

# Or set environment variable
export GITHUB_REPO=owner/repo
```

---

## Example: Complete New Project Setup

```bash
#!/bin/bash
# setup-project.sh - Complete project initialization

REPO="owner/my-new-project"

echo "Setting up $REPO..."

# 1. Setup labels, milestones, project
gh-admin workflow setup-repo \
  --labels \
  --milestones "v0.1,v1.0,v2.0" \
  --project "Development" \
  --repo $REPO

# 2. Create initial issues
gh-admin issue create "Project structure setup" \
  --label "type:feature,priority:high" \
  --milestone "v0.1" \
  --repo $REPO

gh-admin issue create "Write README" \
  --label "type:docs,priority:medium" \
  --milestone "v0.1" \
  --repo $REPO

gh-admin issue create "Setup CI/CD" \
  --label "type:feature,priority:medium" \
  --milestone "v0.1" \
  --repo $REPO

echo "✓ Project setup complete!"
echo "Visit: https://github.com/$REPO"
```

---

**That's it! You're ready to use the GitHub Admin Plugin in your project!** 🚀

For full documentation, see the plugin repository.
