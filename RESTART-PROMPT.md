# ETEx - Restart Prompt for Claude Code

**Use this when starting a new Claude Code session or when context runs out.**

---

## Project Overview

**Project**: ETEx (Engineering Terminology Explorer)
**Purpose**: Multi-language terminology search system across industry standards (NAMUR ↔ IATE ↔ DIN ↔ IEC)
**Timeline**: 6-week MVP sprint
**Current Phase**: Setup & Planning (Week 0)
**Last Updated**: 2025-10-31

---

## Quick Context

### What is ETEx?

ETEx solves terminology inconsistency in German technical documentation (e.g., "Drucksensor" vs "Druckmessumformer"). It's a language-internal thesaurus that maps synonyms within each language and matches terminology across regional/international standards.

### Code Reuse Strategy

We're **reusing proven code** from the Glossary APP project (located at `vendor/glossary-app/`):
- ✅ Import directly when possible (Tier 1)
- ✅ Copy with attribution when modifications needed (Tier 2)
- ✅ Reference for inspiration (Tier 3)

**Don't reinvent the wheel** - check `vendor/glossary-app/` first!

---

## Essential Documentation (Read These First)

### 1. **CLAUDE.md** - Your Operating Manual
**Location**: `./CLAUDE.md`
**What it contains**:
- Global rules for all agents (code reuse, progress tracking, documentation)
- **Scripts Organization Rules** - MANDATORY: Each script = own subfolder + README
- **GitHub Workflow** - Issue lifecycle, closing requirements, project board usage
- Role-specific guidelines (Design, Coding, Review agents)
- Multi-agent handoff protocols

**Start here** if you're implementing features or creating scripts.

---

### 2. **REQUIREMENTS.md** - Product Specification
**Location**: `./docs/REQUIREMENTS.md`
**What it contains**:
- Complete MVP feature list (Week 1-6 breakdown)
- Database schema (13 tables with full specifications)
- API endpoints
- UI mockups and user stories
- Technical stack (Python 3.12, FastAPI, React 18, SQLite, Material-UI)

**Start here** if you're designing features or understanding scope.

---

### 3. **Scripts Organization**
**Location**: `./scripts/`
**Structure**:
```
scripts/
├── app/           # Production runtime scripts
├── dev/
│   ├── setup/     # Initial setup
│   ├── github/    # GitHub automation (labels, issues)
│   │   ├── create-agent-labels/      ← Each script has
│   │   │   ├── create-agent-labels.ps1    own subfolder
│   │   │   └── README.md                  + README!
│   │   └── create-github-labels/
│   ├── testing/   # Test runners
│   └── quality/   # Linters, formatters
├── docs/          # Documentation generation
└── data/          # Database operations
```

**CRITICAL RULE**: Every script MUST have its own subfolder with README.md (see CLAUDE.md line 75)

---

## Current Project Status

### ✅ Completed

1. **Repository Setup**
   - GitHub repo: https://github.com/developer-hhiotsystems/ETEx
   - Local repo synced with remote (master → main)
   - Git submodule for Glossary APP reference (`vendor/glossary-app/`)

2. **Documentation**
   - Complete REQUIREMENTS.md (3,169 lines)
   - Complete CLAUDE.md with agent guidelines
   - Complete scripts organization guide
   - GitHub workflow guide (labels, issues, project board)

3. **GitHub Workflow**
   - 22 labels created (9 essential + 13 agent-specific)
   - Issue templates ready
   - Label creation scripts in proper subfolders

4. **Development Setup**
   - `.gitattributes` and `.editorconfig` for line endings
   - Script structure reorganized (each script = subfolder + README)

### 🔄 In Progress

- GitHub Projects setup (6-week sprint with iterations)
- Milestone creation (Week 1-6)

### ⏳ Not Started (Week 1-6 Implementation)

**Week 1**: Database schema, environment setup
**Week 2**: PDF upload, document processing
**Week 3**: Term extraction
**Week 4**: IATE API integration
**Week 5**: IEC database import, search
**Week 6**: Manual entry, browse UI, polish

---

## Key Decisions (Architecture Decision Records)

**Location**: `./docs/adr/`

- **ADR-0001**: Use Glossary APP as reference project (accepted)
- More ADRs to be created during implementation

---

## Quick Start for Common Tasks

### Starting a New Feature

1. **Read the spec**: `docs/REQUIREMENTS.md` (find your feature in Week 1-6 breakdown)
2. **Check CLAUDE.md**: Follow Design → Coding → Review workflow
3. **Check vendor**: `ls vendor/glossary-app/src/backend/services/` (reuse existing code)
4. **Create issue**: Use GitHub labels, assign to milestone (Week N)

### Creating a New Script

1. **Create subfolder**: `scripts/<category>/<script-name>/`
2. **Add script file**: `<script-name>.ps1`
3. **Add README.md**: Purpose, usage, examples, troubleshooting
4. **Update category README**: Add to script list

See CLAUDE.md line 75 for complete rules.

### Creating GitHub Issue

```bash
gh issue create \
  --title "feat(backend): Your feature" \
  --label "type:feature,priority:high,phase:mvp,component:backend" \
  --milestone "Week 2" \
  --body "See docs/REQUIREMENTS.md section X"
```

---

## Important File Locations

| What | Where |
|------|-------|
| Agent guidelines | `./CLAUDE.md` |
| Product requirements | `./docs/REQUIREMENTS.md` |
| Architecture docs | `./docs/architecture/` |
| Decision records (ADRs) | `./docs/adr/` |
| Reference guides | `./docs/reference/` |
| Setup guides | `./docs/getting-started/` |
| Scripts | `./scripts/` (each in subfolder!) |
| Glossary APP reference | `./vendor/glossary-app/` |
| Agent workspace | `./.agent/workspace/` (gitignored) |
| Agent outputs | `./.agent/outputs/` (committed) |

---

## GitHub Project Board

**Project**: "ETEx MVP - 6 Week Sprint"
**Views**:
- Board (Kanban): To Do → In Progress → Done
- Table: Full issue list with filters
- Roadmap: Timeline showing 6-week sprint

**Milestones**: Week 1-6 (one per week)
**Milestone (overall)**: "v1.0 MVP"

**Issue Lifecycle**: Create → Start (In Progress) → PR → Merge → Close (Done) → Verify

See CLAUDE.md line 761 for complete workflow.

---

## Tech Stack

**Backend**:
- Python 3.12+
- FastAPI (web framework)
- SQLAlchemy 2.0+ (ORM)
- Alembic (migrations)
- SQLite (database)

**Frontend**:
- React 18
- TypeScript
- Material-UI (MUI)
- Vite (build tool)

**External Integrations**:
- IATE API (terminology database)
- IEC Electropedia (22,798 terms)

**Development**:
- pytest (testing)
- GitHub CLI (automation)
- PowerShell scripts (Windows environment)

---

## What to Do Next

**If you're starting fresh**:
1. Read CLAUDE.md (your operating manual)
2. Read REQUIREMENTS.md section 1-5 (overview, MVP scope)
3. Check current GitHub issues: `gh issue list`
4. Ask user: "What should I work on next?"

**If continuing previous work**:
1. Ask user: "What was I working on last?"
2. Check git log: `git log -5 --oneline`
3. Check open issues: `gh issue list --assignee @me`
4. Continue where you left off

**If blocked or unclear**:
1. Check CLAUDE.md for guidelines
2. Check REQUIREMENTS.md for specifications
3. Check vendor/glossary-app/ for reference code
4. Ask user for clarification

---

## Commands You'll Use Often

```bash
# Git
git status
git log -5 --oneline
git commit -m "feat(component): Description"

# GitHub Issues
gh issue list
gh issue list --milestone "Week 2"
gh issue create --title "..." --label "..." --milestone "..."

# GitHub CLI
gh auth status
gh repo view developer-hhiotsystems/ETEx

# Navigation
cd scripts/dev/github/create-agent-labels/
ls vendor/glossary-app/src/backend/services/
```

---

## Red Flags (Things NOT to Do)

❌ **Don't put scripts directly in category folders** (must be in subfolder with README)
❌ **Don't copy code without attribution** (use Tier 2 template in CLAUDE.md)
❌ **Don't create manual status files** (use git commits and GitHub issues)
❌ **Don't skip tests** (80%+ coverage required)
❌ **Don't close issues without verification comment** (see CLAUDE.md line 827)
❌ **Don't implement without reading the spec** (Design → Code → Review)

---

## Contact & Resources

**GitHub Repository**: https://github.com/developer-hhiotsystems/ETEx
**Reference Project**: https://github.com/developer-hhiotsystems/terminology-extraction
**Labels**: https://github.com/developer-hhiotsystems/ETEx/labels
**Issues**: https://github.com/developer-hhiotsystems/ETEx/issues

---

**You're ready to start! Read CLAUDE.md next, then ask the user what to work on.**

---

**Last Updated**: 2025-10-31
**Version**: 1.0
