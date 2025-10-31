# ETEx Scripts Organization

**Purpose**: Clear separation between application scripts and development helper scripts
**Last Updated**: 2025-10-31
**Version**: 1.0

---

## Directory Structure

```
scripts/
├── README.md                          # This file
│
├── app/                               # Application scripts (runtime, production)
│   ├── README.md                      # Application scripts guide
│   ├── start-backend.ps1             # Start FastAPI backend server
│   ├── start-frontend.ps1            # Start React frontend dev server
│   ├── migrate-database.ps1          # Run Alembic migrations
│   └── seed-database.ps1             # Seed database with test data
│
├── dev/                               # Development helper scripts
│   ├── README.md                      # Development scripts guide
│   │
│   ├── setup/                         # Initial setup scripts
│   │   ├── README.md                  # Setup scripts guide
│   │   ├── install-dependencies.ps1   # Install Python + Node deps
│   │   ├── install-gh-cli.ps1        # Install GitHub CLI
│   │   └── setup-environment.ps1      # Create .env from template
│   │
│   ├── github/                        # GitHub workflow helpers
│   │   ├── README.md                  # GitHub scripts guide
│   │   ├── create-agent-labels.ps1    # Create 13 agent labels
│   │   ├── create-essential-labels.ps1 # Create 9 essential labels
│   │   ├── create-week1-issues.ps1    # Create Week 1 issues
│   │   └── setup-project-board.ps1    # Setup GitHub Project board
│   │
│   ├── testing/                       # Testing helper scripts
│   │   ├── README.md                  # Testing scripts guide
│   │   ├── run-all-tests.ps1         # Run unit + integration tests
│   │   ├── run-coverage.ps1          # Run tests with coverage report
│   │   └── watch-tests.ps1           # Watch mode for TDD
│   │
│   └── quality/                       # Code quality scripts
│       ├── README.md                  # Quality scripts guide
│       ├── lint-backend.ps1          # Run flake8, black, pylint
│       ├── lint-frontend.ps1         # Run ESLint, Prettier
│       └── format-all.ps1            # Auto-format all code
│
├── docs/                              # Documentation generation
│   ├── README.md                      # Documentation scripts guide
│   ├── generate-api-docs.ps1         # Generate API reference
│   └── export-to-wiki.ps1            # Export docs to GitHub Wiki
│
└── data/                              # Data management scripts
    ├── README.md                      # Data scripts guide
    ├── backup-database.ps1           # Backup SQLite database
    ├── restore-database.ps1          # Restore from backup
    └── import-iec-terms.ps1          # Import IEC Electropedia CSV
```

---

## Script Categories

### 1. Application Scripts (`scripts/app/`)

**Purpose**: Production/runtime scripts that users run to operate the application

**Characteristics**:
- ✅ Run during normal app usage
- ✅ Documented in user guides
- ✅ Stable APIs (don't change often)
- ✅ Error handling for end users

**Examples**:
- Start servers (backend, frontend)
- Run migrations
- Seed database
- Deploy application

---

### 2. Development Helper Scripts (`scripts/dev/`)

**Purpose**: Scripts for developers during development workflow

**Subdivisions**:

#### **Setup** (`scripts/dev/setup/`)
First-time setup, environment configuration

**Examples**:
- Install dependencies
- Setup .env file
- Install GitHub CLI
- Initialize database

#### **GitHub** (`scripts/dev/github/`)
GitHub workflow automation (issues, labels, boards)

**Examples**:
- Create labels
- Create issues
- Setup project boards
- Create milestones

#### **Testing** (`scripts/dev/testing/`)
Test execution and coverage

**Examples**:
- Run all tests
- Generate coverage reports
- Watch mode for TDD
- Run specific test suites

#### **Quality** (`scripts/dev/quality/`)
Code quality checks and auto-formatting

**Examples**:
- Linters (flake8, ESLint)
- Formatters (black, prettier)
- Type checkers (mypy, tsc)
- Security scanners

---

### 3. Documentation Scripts (`scripts/docs/`)

**Purpose**: Generate or export documentation

**Examples**:
- Generate API docs from code
- Export docs to GitHub Wiki
- Generate changelog from commits
- Create release notes

---

### 4. Data Management Scripts (`scripts/data/`)

**Purpose**: Database and data file operations

**Examples**:
- Backup/restore database
- Import external data (IEC, IATE)
- Export data to CSV
- Database maintenance

---

## Script Naming Conventions

### File Names

**Format**: `<verb>-<noun>.ps1` or `<verb>-<noun>-<detail>.ps1`

**Good Examples**:
```
✅ start-backend.ps1
✅ create-agent-labels.ps1
✅ run-all-tests.ps1
✅ backup-database.ps1
✅ install-gh-cli.ps1
```

**Bad Examples**:
```
❌ script1.ps1                  (not descriptive)
❌ helper.ps1                   (too generic)
❌ createAgentLabels.ps1        (wrong case - use kebab-case)
❌ agent_labels.ps1             (use dashes, not underscores)
```

### Script Headers

**Every script MUST have**:
```powershell
# Script: <descriptive name>
# Purpose: <one-line description>
# Category: app | dev/setup | dev/github | dev/testing | dev/quality | docs | data
# Usage: .\<script-name>.ps1 [parameters]
# Last Updated: YYYY-MM-DD

<#
.SYNOPSIS
    Brief description

.DESCRIPTION
    Detailed description of what this script does

.PARAMETER param1
    Description of parameter

.EXAMPLE
    .\script-name.ps1
    Description of example

.EXAMPLE
    .\script-name.ps1 -param1 value
    Description of example with parameter

.NOTES
    Author: ETEx Development Team
    Version: 1.0.0
#>
```

---

## README.md Requirements

**Every script subdirectory MUST have a README.md** with:

1. **Purpose**: What this category of scripts does
2. **Prerequisites**: What's needed to run these scripts
3. **Script List**: Table of all scripts with descriptions
4. **Usage Examples**: Common workflows using these scripts
5. **Troubleshooting**: Common issues and solutions

**Template**:
```markdown
# <Category> Scripts

**Purpose**: <what these scripts do>

**Prerequisites**:
- <requirement 1>
- <requirement 2>

---

## Available Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `script1.ps1` | <description> | `.\script1.ps1` |
| `script2.ps1` | <description> | `.\script2.ps1 -param value` |

---

## Common Workflows

### Workflow 1: <name>
```powershell
# Step 1
.\script1.ps1

# Step 2
.\script2.ps1
```

---

## Troubleshooting

**Problem**: <issue>
**Solution**: <fix>
```

---

## Script Development Guidelines

### 1. Error Handling

**All scripts MUST**:
```powershell
# Check prerequisites
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "Error: GitHub CLI not found" -ForegroundColor Red
    exit 1
}

# Use try/catch for operations
try {
    # ... operation ...
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
```

### 2. User Feedback

**Provide clear progress**:
```powershell
Write-Host "[1/3] Checking prerequisites..." -ForegroundColor Cyan
Write-Host "  ✓ GitHub CLI found" -ForegroundColor Green

Write-Host "[2/3] Creating labels..." -ForegroundColor Cyan
Write-Host "  ✓ Created 5 labels" -ForegroundColor Green
Write-Host "  ⊙ Skipped 3 existing labels" -ForegroundColor Yellow

Write-Host "[3/3] Complete!" -ForegroundColor Green
```

### 3. Parameters

**Use PowerShell parameters properly**:
```powershell
param(
    [Parameter(Mandatory=$false)]
    [string]$Repo = "developer-hhiotsystems/ETEx",

    [Parameter(Mandatory=$false)]
    [switch]$DryRun,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)
```

### 4. Documentation

**Every script MUST have**:
- Synopsis comment block
- Parameter descriptions
- Usage examples
- Error handling

### 5. Testing

**Test scripts with**:
- `-DryRun` mode (if applicable)
- `-WhatIf` mode (if applicable)
- Error scenarios (missing prerequisites, network errors)
- Success scenarios

---

## Migration Plan for Existing Scripts

### Current Scripts (to reorganize):

```
scripts/
├── github-workflow-simulation.md        → docs/reference/
├── create-week1-issues.md               → docs/reference/
├── install-gh-cli.ps1                   → dev/setup/
├── create-github-labels.ps1             → dev/github/
├── create-agent-labels.ps1              → dev/github/
├── create-agent-labels-safe.ps1         → dev/github/
```

### Migration Steps:

1. Create new directory structure
2. Move scripts to appropriate locations
3. Create README.md for each category
4. Update script headers
5. Update documentation references
6. Test all scripts in new locations
7. Update CLAUDE.md with new structure
8. Delete old scripts from root

---

## Integration with CLAUDE.md

**CLAUDE.md should reference scripts by category**:

```markdown
## Development Workflow

### Setting Up Environment
See: `scripts/dev/setup/README.md`

### Creating GitHub Issues
See: `scripts/dev/github/README.md`

### Running Tests
See: `scripts/dev/testing/README.md`
```

---

## Benefits of This Structure

✅ **Clear Separation**: App vs dev vs docs vs data
✅ **Easy Discovery**: Logical grouping by purpose
✅ **Self-Documenting**: README in every directory
✅ **Scalable**: Easy to add new categories
✅ **Maintainable**: Scripts organized by lifecycle
✅ **Professional**: Standard industry practice

---

## Examples from Other Projects

**Node.js projects**:
```
scripts/
├── build/
├── test/
├── deploy/
└── utils/
```

**Python projects**:
```
scripts/
├── setup/
├── ci/
├── maintenance/
└── tools/
```

**Our approach** follows these patterns with ETEx-specific needs.

---

**End of Scripts Organization Guide**
**Last Updated**: 2025-10-31
**Version**: 1.0
