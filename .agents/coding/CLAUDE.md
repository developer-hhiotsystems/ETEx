# Coding Agent - Instructions

**Role**: Feature Implementation & Testing
**Workspace**: `.agents/workspace/coding/`
**Outputs**: `src/`, `tests/`
**Last Updated**: 2025-10-31

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
