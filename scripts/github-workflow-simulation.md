# GitHub Workflow Simulation

**Purpose**: Step-by-step walkthrough of typical ETEx development scenarios using GitHub Issues, Projects, and PRs
**Last Updated**: 2025-10-31

---

## Scenario 1: Week 1 - Setting Up Database Schema

### Step 1: Create Milestone for Week 1

```bash
gh milestone create "Week 1: Project Setup & Database" \
  --description "Setup development environment, create database schema, initialize React frontend" \
  --due-date "2025-11-07"
```

**Result**: Milestone #1 created

---

### Step 2: Break Down Week 1 into Tasks (Issues)

Create parent tracking issue:

```bash
gh issue create \
  --title "meta: Week 1 - Project Setup & Database (Milestone)" \
  --body "$(cat <<'EOF'
## Week 1 Goals

**Dates**: 2025-10-31 to 2025-11-07

### Tasks
- [ ] #10 - Create database schema with SQLAlchemy models
- [ ] #11 - Setup Alembic migrations
- [ ] #12 - Create Pydantic schemas for request/response validation
- [ ] #13 - Create .env.example and requirements.txt
- [ ] #14 - Initialize React frontend with Vite
- [ ] #15 - Setup vendor/glossary-app reference

### Success Criteria
- All 5 database tables created and migrated
- Development environment fully functional
- Ready for Week 2 (PDF upload)

### Week 1 Completion
- [ ] All tasks complete
- [ ] Tests passing (80%+ coverage)
- [ ] Documentation updated
- [ ] Git commit: "Week 1 complete"
EOF
)" \
  --label "type: meta,phase: mvp,priority: high" \
  --milestone "Week 1: Project Setup & Database"
```

**Result**: Issue #9 created (meta-issue tracking Week 1)

---

### Step 3: Create Individual Task Issues

**Task 1: Database Schema**

```bash
gh issue create \
  --title "feat(backend): Create database schema with SQLAlchemy models (Week 1)" \
  --body "$(cat <<'EOF'
## Feature Overview
Implement the 5 core database tables using SQLAlchemy ORM as defined in docs/REQUIREMENTS.md section 13.

## Acceptance Criteria
- [ ] authoritative_sources table (12 fields, tier enum, config JSON)
- [ ] terms table (14 fields, full-text search index)
- [ ] term_synonyms table (bidirectional relationship)
- [ ] translations table (source/target language validation)
- [ ] uploaded_documents table (file tracking, processing status)
- [ ] All foreign keys with proper cascade behavior
- [ ] Indexes for performance (source_id, language_code)
- [ ] Timestamps auto-managed (created_at, updated_at)

## Related Spec
docs/REQUIREMENTS.md section 13

## Implementation Notes
- Reference vendor/glossary-app/src/backend/models/base_models.py (Tier 3)
- Use SQLAlchemy 2.0+ syntax
- Store database at data/database/etex.db (gitignored)
- Create models in src/backend/models/

## Week / Phase
Week 1 / MVP Phase 1

## Dependencies
None (first task)

## Blocks
#11 (Alembic migrations)
#17 (API endpoints - Week 2)

## Estimated Effort
🔶 Large (1-2 days)
EOF
)" \
  --label "type: feature,priority: high,phase: mvp,component: backend" \
  --milestone "Week 1: Project Setup & Database"
```

**Result**: Issue #10 created

---

**Task 2: Alembic Migrations**

```bash
gh issue create \
  --title "feat(backend): Setup Alembic database migrations (Week 1)" \
  --body "$(cat <<'EOF'
## Feature Overview
Setup Alembic for database schema versioning and migrations.

## Acceptance Criteria
- [ ] alembic.ini configured
- [ ] alembic/env.py setup with ETEx models
- [ ] Initial migration created (001_initial_schema.py)
- [ ] Migration runs successfully (alembic upgrade head)
- [ ] Database created at data/database/etex.db
- [ ] Rollback works (alembic downgrade base)

## Implementation Notes
- Follow Alembic best practices
- Auto-generate migration from models
- Test upgrade/downgrade cycle

## Week / Phase
Week 1 / MVP

## Dependencies
Depends on #10 (database schema must exist first)

## Estimated Effort
🔹 Small (< 4 hours)
EOF
)" \
  --label "type: feature,priority: high,phase: mvp,component: backend" \
  --milestone "Week 1: Project Setup & Database"
```

**Result**: Issue #11 created

---

### Step 4: Add Issues to Project Board

```bash
# Create project board
gh project create --title "ETEx MVP - 6 Week Sprint" \
  --body "Track all MVP tasks (Week 1-6)"

# Add issues to project (assuming project ID = 1)
gh project item-add 1 --owner developer-hhiotsystems --content-id <issue-10-id>
gh project item-add 1 --owner developer-hhiotsystems --content-id <issue-11-id>
```

**Result**: Issues appear in "Backlog" column on project board

---

### Step 5: Start Working on Task (Move to In Progress)

```bash
# Assign yourself to issue
gh issue edit 10 --add-assignee "@me"

# Add status label
gh issue edit 10 --add-label "status: in-progress"

# Comment on issue to log progress
gh issue comment 10 --body "Started implementation. Creating SQLAlchemy models in src/backend/models/"
```

**Result**: Issue #10 shows assigned to you, moved to "In Progress" column

---

### Step 6: Implement Feature (Coding)

```bash
# Create feature branch
git checkout -b feat/database-schema

# Create model files
# (implementation work happens here)

# Commit work
git add src/backend/models/
git commit -m "feat(backend): Implement SQLAlchemy models for 5 core tables

- Created authoritative_source.py (12 fields, tier enum)
- Created term.py (14 fields, full-text search support)
- Created term_synonym.py (bidirectional relationship)
- Created translation.py (language validation)
- Created uploaded_document.py (file tracking)
- Added indexes for performance
- All foreign keys with cascade behavior

Related to #10
Progress: Week 1 - 40% complete"
```

---

### Step 7: Create Pull Request

```bash
gh pr create \
  --title "feat(backend): Implement database schema with SQLAlchemy models (Week 1)" \
  --body "$(cat <<'EOF'
## Summary
Implements 5 core database tables using SQLAlchemy ORM per requirements.

## Changes Made
- Created SQLAlchemy models in src/backend/models/
- Added database config in src/backend/core/database.py
- Created .env.example with DATABASE_URL
- Added unit tests for models (95% coverage)

## Related Issues
Closes #10
Blocks #11 (Alembic migrations)

## Testing
- [x] Unit tests pass (pytest tests/unit/backend/models/)
- [x] Coverage: 95% (target: 80%)
- [x] Manual verification: Created sample data

## Review Checklist
- [x] Code follows PEP 8 (black, flake8)
- [x] All foreign keys have cascade behavior
- [x] Indexes added for performance
- [x] No hardcoded secrets

## Code Reuse
- [x] Tier 3: Referenced vendor/glossary-app patterns, implemented from scratch
EOF
)" \
  --label "type: feature,component: backend" \
  --assignee "@me"
```

**Result**: PR #16 created, linked to issue #10

---

### Step 8: Self-Review and Merge

```bash
# Run full test suite
pytest tests/unit/backend/models/ --cov

# Check code quality
black src/backend/models/
flake8 src/backend/models/

# If all good, merge PR
gh pr merge 16 --squash --delete-branch

# PR merge automatically closes issue #10
```

**Result**:
- PR #16 merged
- Issue #10 automatically closed
- Branch `feat/database-schema` deleted
- Issue moved to "Done" column

---

### Step 9: Update Week 1 Meta-Issue

```bash
gh issue comment 9 --body "✅ Task #10 complete (Database schema implemented)

Progress: 1/6 tasks done (16% Week 1 complete)"

# Check off task in meta-issue (manual edit on GitHub UI or via API)
```

---

### Step 10: Repeat for Remaining Tasks

Continue with issues #11, #12, #13, #14, #15 following same workflow.

---

## Scenario 2: Week 2 - Bug Discovered During PDF Upload

### Step 1: Discover Bug During Testing

While implementing PDF upload (Week 2), you discover that scanned PDFs crash the extractor.

### Step 2: Create Bug Issue

```bash
gh issue create \
  --title "bug(extraction): PDF parser fails on scanned NAMUR NE107 documents" \
  --body "$(cat <<'EOF'
## Bug Description
When uploading scanned NAMUR NE107 PDF, the extractor crashes with IndexError.

## Steps to Reproduce
1. Upload tests/fixtures/namur-ne107-scanned.pdf
2. Click "Extract Terms"
3. Observe error

## Expected Behavior
Show error: "Scanned PDFs not supported yet. OCR coming in Phase 2."

## Actual Behavior
Crashes with IndexError: list index out of range

## Error Log
```
[2025-11-08 10:15:23] ERROR: PDF extraction failed
Traceback (most recent call last):
  File "src/backend/services/extraction/pdf_processor.py", line 45
  ...
IndexError: list index out of range
```

## Environment
- Python 3.12.0
- Windows 11
- pdf_extractor.py from Glossary APP

## Impact
🟠 High - Affects Week 2 milestone, but scanned PDFs are edge case (5% of docs)

## Proposed Fix
1. Add is_scanned_pdf() check before extraction
2. Return friendly error if scanned
3. Add unit test for scanned PDF handling
4. Document limitation in MVP exclusions

## Related Issues
Blocks #18 (Week 2 completion)
Future: #45 (Phase 2C - OCR support)
EOF
)" \
  --label "type: bug,priority: high,component: extraction" \
  --milestone "Week 2: Document Upload & PDF Processing"
```

**Result**: Issue #23 created

---

### Step 3: Prioritize Bug Fix

```bash
# Add to project board
gh project item-add 1 --owner developer-hhiotsystems --content-id <issue-23-id>

# Assign to yourself
gh issue edit 23 --add-assignee "@me"

# Mark as in-progress
gh issue edit 23 --add-label "status: in-progress"
```

---

### Step 4: Fix Bug

```bash
# Create fix branch
git checkout -b fix/scanned-pdf-handling

# Implement fix
# (add is_scanned_pdf() check, return error)

# Add test
# (test with scanned PDF fixture)

# Commit
git add src/backend/services/extraction/pdf_processor.py
git add tests/unit/backend/test_pdf_processor.py
git commit -m "fix(extraction): Handle scanned PDFs gracefully

- Added is_scanned_pdf() detection using PyPDF2
- Return friendly error message instead of crash
- Added unit test for scanned PDF handling
- Documented MVP limitation in docs/REQUIREMENTS.md

Fixes #23"
```

---

### Step 5: Create PR for Bug Fix

```bash
gh pr create \
  --title "fix(extraction): Handle scanned PDFs gracefully (Fixes #23)" \
  --body "$(cat <<'EOF'
## Summary
Prevents crash when users upload scanned (image-based) PDFs.

## Changes Made
- Added is_scanned_pdf() detection function
- Return 400 Bad Request with friendly error message
- Added unit test for scanned PDF handling
- Updated docs/REQUIREMENTS.md MVP exclusions

## Related Issues
Fixes #23

## Testing
- [x] Unit test added (test_scanned_pdf_handling)
- [x] All tests pass
- [x] Manual test: Uploaded NAMUR-NE107-scanned.pdf, received error message

## Review Checklist
- [x] Code follows PEP 8
- [x] Error message is user-friendly
- [x] Test added for edge case
EOF
)" \
  --label "type: bug,component: extraction"
```

**Result**: PR #24 created

---

### Step 6: Merge Bug Fix

```bash
# Run tests
pytest tests/unit/backend/test_pdf_processor.py

# Merge
gh pr merge 24 --squash --delete-branch
```

**Result**: Bug #23 closed, PR #24 merged

---

## Scenario 3: Planning Change - Defer Feature to Phase 2

### Step 1: Realize Week 3 is Overloaded

During Week 2, you realize synonym auto-detection (planned for Week 3) is too complex for MVP.

### Step 2: Create Planning Issue

```bash
gh issue create \
  --title "planning: Defer synonym auto-detection to Phase 2E" \
  --body "$(cat <<'EOF'
## Change Proposal
Move synonym auto-detection from Week 3 (MVP) to Phase 2E (post-MVP).

## Rationale
Week 3 is overloaded:
- Term extraction more complex than estimated (multi-language PDFs)
- Manual synonym linking via UI sufficient for MVP
- Auto-detection requires NLP (spaCy embeddings) = extra complexity

## Impact on MVP
✅ MVP still achieves goal: Users can manually link synonyms via UI
❌ No auto-detection: Users must identify synonyms themselves (acceptable for MVP)

## Updated Week 3 Scope

**Remove**:
- [ ] Synonym auto-detection algorithm
- [ ] spaCy word embeddings
- [ ] Co-occurrence analysis

**Keep**:
- [x] Term extraction from PDFs
- [x] Manual term review UI
- [x] Manual synonym linking UI

## Updated docs/REQUIREMENTS.md
Section 10 (MVP Scope) - move synonym auto-detection to EXCLUDES list

## Dependencies
- Update #22 (Week 3 tasks) to remove auto-detection subtasks
- Create #67 (Phase 2E - Synonym Auto-Detection)

## Approval Needed
Please review and comment if this scope change is acceptable.
EOF
)" \
  --label "type: planning,priority: medium,phase: mvp"
```

**Result**: Issue #50 created

---

### Step 3: Discuss and Approve

```bash
# Add comment approving change (simulating decision)
gh issue comment 50 --body "✅ Approved. Manual synonym linking is sufficient for MVP. Auto-detection deferred to Phase 2E.

Action items:
1. Update docs/REQUIREMENTS.md section 10
2. Close #22 subtasks related to auto-detection
3. Create #67 for Phase 2E tracking"
```

---

### Step 4: Update Documentation

```bash
# Create branch for doc update
git checkout -b docs/update-mvp-scope

# Edit docs/REQUIREMENTS.md
# (move synonym auto-detection from INCLUDES to EXCLUDES)

# Commit
git commit -am "docs: Defer synonym auto-detection to Phase 2E

- Updated MVP scope (section 10)
- Moved auto-detection to EXCLUDES
- Added to Phase 2E roadmap (section 17)
- Updated Week 3 tasks in implementation plan

Closes #50"

# Push and create PR
git push origin docs/update-mvp-scope
gh pr create --title "docs: Update MVP scope - defer synonym auto-detection" \
  --body "Closes #50"

# Merge
gh pr merge --squash
```

**Result**: Planning change documented and approved

---

## Scenario 4: Week 6 - MVP Complete, Create Release

### Step 1: Verify All Week 1-6 Tasks Complete

```bash
# Check for open issues in MVP milestone
gh issue list --milestone "Week 6: Manual Entry, Browse & Polish" --state open

# If none, proceed with release prep
```

---

### Step 2: Create Release Checklist Issue

```bash
gh issue create \
  --title "release: Prepare v0.1.0 MVP Release" \
  --body "$(cat <<'EOF'
## Release Checklist

### Code Quality
- [ ] All tests passing (pytest tests/)
- [ ] Coverage ≥ 80% (pytest --cov)
- [ ] No critical bugs open
- [ ] Code reviewed (all PRs merged)

### Documentation
- [ ] README.md updated (features, setup, usage)
- [ ] CHANGELOG.md created (all features, fixes since start)
- [ ] API documentation complete (Wiki)
- [ ] Setup guide verified (docs/getting-started/SETUP.md)

### Functionality
- [ ] IATE API integration working
- [ ] PDF upload and extraction working (NAMUR)
- [ ] IEC database imported (22,798 terms)
- [ ] Manual term entry working
- [ ] Search and browse working
- [ ] All MVP acceptance criteria met (docs/REQUIREMENTS.md section 15)

### Release Tasks
- [ ] Create CHANGELOG.md
- [ ] Tag release v0.1.0
- [ ] Create GitHub Release with notes
- [ ] Update roadmap (mark Phase 1 complete)

### Post-Release
- [ ] Announce release (if applicable)
- [ ] Plan Phase 2A kickoff
EOF
)" \
  --label "type: release,priority: high,phase: mvp"
```

**Result**: Issue #100 created

---

### Step 3: Create CHANGELOG.md

```bash
# Create changelog
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to ETEx will be documented in this file.

## [0.1.0] - 2025-12-12 (MVP Release)

### Added (Features)
- Database schema with 5 core tables (authoritative_sources, terms, term_synonyms, translations, uploaded_documents)
- PDF upload and term extraction for NAMUR standards
- IATE API integration for EU terminology
- IEC Electropedia database import (22,798 terms, 92.4% German coverage)
- Manual term entry interface
- Search functionality with filters (source, language)
- Browse by source and language
- Multi-language support (German/English)

### Fixed (Bugs)
- #23: PDF parser crash on scanned documents
- #34: IATE API rate limiting errors
- #56: Search results pagination issues

### Changed (Updates)
- #50: Deferred synonym auto-detection to Phase 2E
- Updated MVP scope (docs/REQUIREMENTS.md section 10)

### Documentation
- Complete API reference in GitHub Wiki
- Setup guide (docs/getting-started/SETUP.md)
- Code reuse strategy guide (docs/reference/code-reuse-strategy.md)
- GitHub workflow guide (docs/reference/github-workflow-guide.md)

### Testing
- 320 unit tests
- 45 integration tests
- 82% test coverage

## [Unreleased] - Phase 2 Roadmap
- Phase 2A: Internal document processing
- Phase 2B: Deviation checking
- Phase 2C: DeepL integration
- Phase 2D: Additional languages (Spanish, Czech, Chinese)
- Phase 2E: Synonym auto-detection
- Phase 2F: User accounts and permissions
EOF

git add CHANGELOG.md
git commit -m "docs: Add CHANGELOG for v0.1.0 MVP release"
git push
```

---

### Step 4: Create Git Tag and GitHub Release

```bash
# Create annotated tag
git tag -a v0.1.0 -m "ETEx MVP Release v0.1.0

First production-ready release with core functionality:
- IATE, NAMUR, IEC authoritative source integration
- PDF upload and term extraction
- Search and browse interface
- Multi-language support (German/English)

6-week MVP development complete.
See CHANGELOG.md for full details."

# Push tag
git push origin v0.1.0

# Create GitHub Release
gh release create v0.1.0 \
  --title "ETEx v0.1.0 - MVP Release" \
  --notes "$(cat <<'EOF'
# ETEx v0.1.0 - MVP Release 🎉

**Engineering Terminology Explorer** - Multi-language terminology search and translation system

## What's New

This is the first MVP release of ETEx, completing the 6-week development sprint.

### Core Features
✅ **Authoritative Source Integration**
- IATE (EU Terminology) - API integration
- NAMUR (Process Automation) - PDF upload & extraction
- IEC Electropedia - Database import (22,798 terms)
- Manual entry interface

✅ **Multi-Language Support**
- German & English (primary pair)
- Ready for Phase 2 language expansion

✅ **Language-Internal Thesaurus**
- Map synonyms within same language
- Cross-standard terminology matching

✅ **Search & Browse**
- Multiple search modes
- Filter by source and language
- Browse functionality

## Installation

See [Setup Guide](docs/getting-started/SETUP.md) for detailed instructions.

Quick start:
```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app:app --reload
```

## Documentation
- [User Guide](https://github.com/developer-hhiotsystems/ETEx/wiki)
- [API Reference](https://github.com/developer-hhiotsystems/ETEx/wiki/API-Reference)
- [Requirements](docs/REQUIREMENTS.md)

## What's Next (Phase 2)
- Internal document processing
- Deviation checking
- DeepL integration
- Additional languages
- Synonym auto-detection
- User accounts

## Metrics
- 320 unit tests
- 45 integration tests
- 82% test coverage
- 22,798 IEC terms imported
- 6 weeks development time

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)
EOF
)"
```

**Result**: GitHub Release v0.1.0 created with release notes

---

### Step 5: Close Release Issue

```bash
gh issue close 100 --comment "✅ MVP Release v0.1.0 complete!

- All checklist items completed
- Release tagged and published
- Documentation updated
- Phase 1 officially complete

Next: Plan Phase 2A kickoff meeting"
```

---

## Summary of Simulated Workflow

### Issues Created
- **Meta-issue** (#9): Week 1 milestone tracker
- **Feature issues** (#10, #11, #12, etc.): Individual tasks
- **Bug issue** (#23): Scanned PDF handling
- **Planning issue** (#50): Scope change decision
- **Release issue** (#100): Release checklist

### Pull Requests Created
- **PR #16**: Database schema implementation
- **PR #24**: Bug fix for scanned PDFs
- **PR #60**: Documentation scope update
- **PR #95**: CHANGELOG for release

### Project Board States
```
Backlog → Ready → In Progress → Review → Done
```
Issues flowed through board as work progressed.

### Labels Used
- `type:` feature, bug, docs, planning, release
- `priority:` critical, high, medium, low
- `phase:` mvp, phase-2a, future
- `component:` backend, frontend, extraction, etc.
- `status:` planning, ready, in-progress, review, blocked

### Milestones Tracked
- Week 1: Project Setup & Database
- Week 2: Document Upload & PDF Processing
- ...
- Week 6: Manual Entry, Browse & Polish

---

## Key Takeaways

1. **Issues = Actionable Tasks**: Every piece of work tracked
2. **PRs = Code Review**: Even solo developer benefits from PR workflow
3. **Project Board = Visual Progress**: Easy to see what's done/in-progress
4. **Labels = Organization**: Filter and prioritize easily
5. **Milestones = Time Tracking**: Week-by-week progress
6. **Planning Issues = Decisions**: Document scope changes
7. **Release Issues = Launch Checklist**: Ensure nothing missed

---

**End of Simulation**
**Last Updated**: 2025-10-31
