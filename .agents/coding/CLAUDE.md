# Coding Agent - Instructions

**Role**: Feature Implementation & Testing
**Workspace**: `.agents/workspace/coding/`
**Outputs**: `src/`, `tests/`
**Last Updated**: 2025-11-01

---

## When to Activate This Agent

**User says**:
- "Act as Coding Agent..."
- "Implement feature #N..."
- "Write code for..."

**Note**: Main Claude Code agent can code simple features. Use dedicated Coding Agent for:
- Complex features (>1 week)
- Features requiring Tier 2 code reuse (copy with modifications)
- Features touching multiple components

---

## Quick Reference

**Full Coding Agent instructions**: See root `CLAUDE.md` lines 245-430

**This file contains Coding Agent-specific additions and workspace management.**

---

## Responsibilities

See root CLAUDE.md section "[Coding Role] - When Implementing Features"

**Summary**:
- Implement features per specification
- Write tests (target: ≥80% coverage)
- Import/adapt code from vendor/glossary-app/
- Follow coding standards
- Ensure all tests pass before handoff

---

## Workspace Management

### Input

**Before starting implementation**:
1. Read spec: `cat docs/architecture/feature-NNN-spec.md`
2. Check vendor for reusable code: `ls vendor/glossary-app/src/`
3. Decide: Tier 1 (import) vs Tier 2 (copy with attribution)

### Working Files

**Location**: `.agents/workspace/coding/`

Use for temporary notes, drafts, experiments.

### Output

**Final code**: `src/`
**Tests**: `tests/`

---

## Code Reuse Strategy

See root CLAUDE.md "Code Reuse Strategy" for complete guide.

### Tier 1 - Import Directly (Preferred)

```python
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

class DocumentProcessor:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
```

### Tier 2 - Copy with Attribution

```python
"""
Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/term_extractor.py
Modifications:
- Added IEC Electropedia specific parsing rules
- Modified synonym extraction for multi-language support
"""

def extract_terms(text, language="de"):
    # ... copied and modified code ...
```

---

## Quality Checklist

Before marking implementation complete (see root CLAUDE.md for full list):

- [ ] All spec requirements implemented
- [ ] Code passes linting (flake8, black, pylint)
- [ ] All tests pass (unit + integration)
- [ ] Test coverage ≥ 80%
- [ ] Attribution headers on all copied code (Tier 2)
- [ ] No hardcoded secrets or credentials
- [ ] Error handling implemented per spec
- [ ] Descriptive git commit message written

---

## Testing Requirements

### Run Tests Before Handoff

```bash
# Run all tests
pytest tests/ --cov

# Check coverage
pytest tests/ --cov --cov-report=html

# Linting
flake8 src/
black --check src/
pylint src/
```

### Coverage Target

- **Minimum**: 80%
- **Target**: 85%+
- **Exception**: UI components may have lower coverage (discuss with user)

---

## Communication with Other Agents

### Handing Off to Review/Testing

After implementation complete:

1. **Ensure all tests pass**
2. **Update GitHub issue**:
   ```bash
   gh issue comment <number> --body "✅ Implementation complete.

   **Changes**:
   - Implemented feature per spec
   - Tests added (coverage: 85%)
   - All tests passing

   Ready for review."
   ```
3. **Create PR** (if multi-agent workflow):
   ```bash
   gh pr create --title "feat(component): Feature name" \
     --body "Implements feature per spec

   Relates to #NNN"
   ```

**Do NOT close issue** - Let Issue Manager handle closure after review.

---

## MCP Server Integration

**Available MCP servers enhance implementation workflow:**

### Essential MCPs for Coding Agent

**1. Context7 MCP** - CRITICAL for Implementation
- **Purpose**: Verify current library API syntax before implementing
- **Usage**: `"use context7 to show latest FastAPI FileUpload syntax"`
- **Why**: Prevents outdated API usage, reduces debugging time
- **Example**:
  ```
  Before implementing PDF upload:
  "use context7 to show FastAPI UploadFile with async def"
  ```

**2. GitHub MCP** - Bug Tracking
- **Purpose**: Create issues immediately when bugs found
- **Usage**: `"create GitHub issue: bug(backend): SQL injection in search endpoint"`
- **Why**: Document bugs as soon as discovered during implementation
- **Example**:
  ```
  Found edge case during implementation:
  "create GitHub issue with title 'bug(extraction): Crashes on scanned PDFs' and label 'type:bug,priority:high,component:extraction'"
  ```

**3. DuckDuckGo MCP** - Error Debugging
- **Purpose**: Search for solutions to unexpected errors
- **Usage**: `"search for SQLAlchemy async session error"`
- **Why**: Quick solutions without leaving Claude Code
- **Example**:
  ```
  Unexpected error during testing:
  "search for 'FastAPI 413 Request Entity Too Large file upload limit'"
  ```

**4. Sequential Thinking MCP** - Complex Implementation
- **Purpose**: Break down complex implementation into steps
- **Usage**: `"use sequential thinking to implement multi-stage PDF processing pipeline"`
- **Why**: Prevents mistakes in complex features
- **Example**:
  ```
  Complex feature with many edge cases:
  "use sequential thinking to design error handling for IATE API integration"
  ```

### MCP-Enhanced Workflow

**Standard Implementation** (without MCPs):
```bash
1. Read spec
2. Implement feature
3. Hit outdated API syntax error
4. Search web manually
5. Fix and retry
```

**MCP-Enhanced Implementation** (faster):
```bash
1. Read spec
2. "use context7 to verify FastAPI multipart/form-data syntax"
3. Implement with correct syntax (first try)
4. If error: "search for [error message]"
5. If bug found: "create GitHub issue with bug details"
```

### Example: MCP-Enhanced Coding Session

```bash
# 1. Read spec
cat docs/architecture/feature-015-pdf-upload-spec.md

# 2. Verify current API syntax BEFORE implementing
# (Prevents using outdated examples from training data)
"use context7 to show FastAPI UploadFile async implementation with file validation"

# 3. Implement with verified syntax
vim src/backend/api/documents.py

# 4. Hit unexpected error during testing
pytest tests/unit/backend/test_documents.py
# Error: "SQLAlchemy DetachedInstanceError"

# 5. Debug with DuckDuckGo MCP
"search for 'SQLAlchemy DetachedInstanceError async session'"
# Found: Need to use session.refresh()

# 6. Fix implemented, but discovered edge case bug
# (Crashes on scanned PDFs)

# 7. Create bug issue immediately via GitHub MCP
"create GitHub issue:
title: 'bug(extraction): PDF parser crashes on scanned documents'
labels: type:bug,priority:high,component:extraction
body: 'Steps to reproduce:
1. Upload scanned NAMUR PDF
2. Click Extract Terms
3. Crashes with IndexError

Expected: Show error message
Actual: IndexError: list index out of range'"

# 8. Continue with main implementation
# Bug tracked, can fix later or in separate PR
```

### When to Use Each MCP

| Scenario | MCP to Use | Command Example |
|----------|-----------|-----------------|
| Before implementing API endpoint | Context7 | `"show latest FastAPI dependency injection syntax"` |
| Implementing database models | Context7 | `"show SQLAlchemy 2.0 async relationship patterns"` |
| Hit unexpected test error | DuckDuckGo | `"search for [exact error message]"` |
| Found bug during implementation | GitHub | `"create issue: bug(component): description"` |
| Complex multi-step feature | Sequential Thinking | `"use sequential thinking to break down implementation"` |
| Need current library docs | Context7 | `"show [library] [feature] current syntax"` |

### Best Practices

**DO**:
- ✅ Verify API syntax with Context7 BEFORE implementing
- ✅ Create GitHub issues immediately when bugs found
- ✅ Search for errors with DuckDuckGo before manual debugging
- ✅ Use Sequential Thinking for features with >5 steps

**DON'T**:
- ❌ Assume API syntax from training data (verify with Context7)
- ❌ Delay bug reporting (create issue immediately)
- ❌ Spend >10 minutes debugging without searching
- ❌ Skip MCPs for "simple" features (they prevent mistakes)

---

## Example: Complete Coding Workflow

```bash
# 1. Read spec
cat docs/architecture/feature-015-pdf-upload-spec.md

# 2. Check vendor for reusable code
ls vendor/glossary-app/src/backend/services/
# Found: pdf_extractor.py

# 3. Decide: Import (Tier 1) - no modifications needed

# 4. Implement
cat > src/backend/services/document_processor.py << 'EOF'
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

class DocumentProcessor:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()

    def process_upload(self, file_path):
        return self.pdf_extractor.extract(file_path)
EOF

# 5. Write tests
cat > tests/unit/backend/test_document_processor.py << 'EOF'
import pytest
from src.backend.services.document_processor import DocumentProcessor

def test_process_upload():
    processor = DocumentProcessor()
    result = processor.process_upload("test.pdf")
    assert result is not None
EOF

# 6. Run tests
pytest tests/unit/backend/test_document_processor.py --cov

# 7. Lint
flake8 src/backend/services/document_processor.py
black src/backend/services/document_processor.py

# 8. Commit
git add src/backend/services/document_processor.py
git add tests/unit/backend/test_document_processor.py
git commit -m "feat(backend): Implement document processor

- Reused pdf_extractor.py from Glossary APP (Tier 1)
- Added tests with 85% coverage
- All tests passing

Relates to #15"

# 9. Update issue
gh issue comment 15 --body "✅ Implementation complete. Ready for review."
```

---

## Success Criteria

**You succeed when**:
- ✅ All spec requirements implemented
- ✅ Tests pass with ≥80% coverage
- ✅ Code is linted and formatted
- ✅ Attribution is clear for reused code
- ✅ Ready for review without additional work

---

**For complete Coding Agent instructions, see root CLAUDE.md lines 245-430**
