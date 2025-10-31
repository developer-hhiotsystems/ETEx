# Code Reuse Strategy from Glossary APP

**Purpose**: Guide for reusing proven components from the Glossary APP project

**Glossary APP Location**: `vendor/glossary-app/` (git submodule)

---

## Overview

The Glossary APP contains production-ready components that solve problems identical to ETEx. Instead of rewriting from scratch, we **reference, import, or adapt** these components.

---

## Three-Tier Strategy

### Tier 1: Import Directly (Preferred)

**When to use**: Component works perfectly as-is, no modifications needed

**How**:
```python
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

# Use directly
extractor = PDFExtractor()
result = extractor.extract(pdf_path)
```

**Benefits**:
- ✅ Zero maintenance (vendor handles updates)
- ✅ Proven stability (100+ test cases)
- ✅ No code duplication

**Drawbacks**:
- ❌ Can't modify behavior
- ❌ Vendor updates might break compatibility

---

### Tier 2: Copy with Attribution (When Modifications Needed)

**When to use**: Component needs ETEx-specific modifications

**How**:
```python
"""
Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/pdf_extractor.py
Modifications:
- Added IEC Electropedia specific PDF parsing rules
- Modified page reference extraction for standards documents
- Added support for multilingual PDF metadata
"""

class PDFExtractor:
    # ... copied code with modifications ...
```

**Requirements**:
- ✅ Attribution header with date
- ✅ Original file path
- ✅ List of modifications
- ✅ Document in CHANGELOG.md

**Benefits**:
- ✅ Can customize for ETEx needs
- ✅ Still gives credit to original work
- ✅ Easy to sync improvements later

**Drawbacks**:
- ❌ Must maintain manually
- ❌ Vendor updates don't apply automatically

---

### Tier 3: Reference Only (Inspiration)

**When to use**: Using as inspiration, not copying code

**How**: Document in this file

**Example**:
> "BilingualCard component (vendor/glossary-app/src/frontend/src/components/BilingualCard.tsx) demonstrates synchronized scrolling pattern. We adapted the concept for our MultiSourceCard component but implemented from scratch."

**Benefits**:
- ✅ Learn from proven patterns
- ✅ No code duplication
- ✅ Full creative control

---

## Available Components

### Backend Services

#### PDF Extractor (Tier 1 - Import Directly) ✅

**Location**: `vendor/glossary-app/src/backend/services/pdf_extractor.py`

**Status**: Production-ready

**Quality**: EXCELLENT
- 100+ test cases validated
- Handles OCR artifacts
- Encoding error normalization
- Page-by-page extraction

**Reuse Strategy**: **Import as-is** (Tier 1)

**Code Example**:
```python
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

class DocumentProcessor:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()

    def process_namur_standard(self, pdf_path):
        return self.pdf_extractor.extract(pdf_path)
```

**Tests Available**: Yes (`vendor/glossary-app/tests/unit/backend/test_pdf_extractor.py`)

---

#### Term Extractor (Tier 2 - Copy Utilities) ⚠️

**Location**: `vendor/glossary-app/src/backend/services/term_extractor.py`

**Status**: Good with caveats

**Quality**: GOOD
- NLP-based term extraction with spaCy
- Multi-language support (EN/DE)
- Frequency-based filtering
- Confidence scoring

**Caveat**: Full file is 564 lines with spaCy dependency

**Reuse Strategy**: **Copy utilities only** (Tier 2)

**What to copy**:
- `clean_term()` - Text normalization
- `strip_leading_articles()` - Remove "the", "der", "die", "das"
- Regex patterns for term validation

**What NOT to copy**:
- Full NLP pipeline (too heavy)
- spaCy integration (ETEx may use different NLP)

**Code Example**:
```python
"""
Utilities adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/term_extractor.py
Modifications:
- Extracted only clean_term() and strip_leading_articles()
- Removed spaCy dependency
- Added chemical engineering specific patterns
"""

def clean_term(term: str) -> str:
    # ... copied from vendor ...
    pass

def strip_leading_articles(term: str, language: str) -> str:
    # ... copied from vendor ...
    pass
```

---

#### DeepL Client (Tier 1 - Import for Phase 2) 🔮

**Location**: `vendor/glossary-app/src/backend/services/translation/clients/deepl_client.py`

**Status**: Production-ready

**Quality**: GOOD
- DeepL API integration
- Batch translation
- Glossary support
- Usage tracking & quota checking

**Reuse Strategy**: **Import directly** (Tier 1) - **Phase 2 only**

**Note**: ETEx MVP focuses on authoritative sources. DeepL is Tier 2 translation source, deferred to Phase 2.

**Future Code Example** (Phase 2):
```python
from vendor.glossary_app.src.backend.services.translation.clients.deepl_client import DeepLClient

# Use when no authoritative translation exists
client = DeepLClient(api_key=config.deepl_api_key)
fallback_translation = client.translate(term, source="de", target="en")
```

---

#### Base Models (Tier 2 - Adapt Schema) 📝

**Location**: `vendor/glossary-app/src/backend/base_models.py`

**Status**: Excellent SQLAlchemy models

**What's Useful**:
- `GlossaryEntry` model → Adapt to ETEx `Term` model
- `UploadedDocument` model → Reuse as-is
- `TranslationHistory` → Adapt to ETEx `Translation` model
- `TermDocumentReference` → Reuse for PDF page references

**Reuse Strategy**: **Reference schema, write new models** (Tier 3/Tier 2 hybrid)

**Approach**:
1. Read `vendor/glossary-app/src/backend/base_models.py`
2. Understand table structure and relationships
3. Write new ETEx models inspired by schema
4. Adapt field names for ETEx domain (e.g., add `source_id`, `confidence`)

**Example**:
```python
# ETEx: src/backend/models/term.py
# Inspired by vendor/glossary-app/src/backend/base_models.py:GlossaryEntry

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from .base import Base

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True)
    term = Column(String(500), nullable=False, index=True)
    language_code = Column(String(10), nullable=False, index=True)
    definition = Column(Text)
    source_id = Column(Integer, ForeignKey("authoritative_sources.id"))  # NEW
    confidence = Column(Float, default=1.0)  # NEW

    # Similar structure to GlossaryEntry but adapted for ETEx
```

---

### Frontend Components

#### BilingualCard Component (Tier 2 - Adapt for Multi-Source) 🎨

**Location**: `vendor/glossary-app/src/frontend/src/components/BilingualCard.tsx`

**Status**: Excellent React component

**Quality**: EXCELLENT
- Side-by-side EN/DE display
- Synchronized scrolling
- Language toggle
- Selection checkboxes
- Clean, responsive design

**Reuse Strategy**: **Copy and adapt** (Tier 2)

**Modifications Needed for ETEx**:
- Support 3+ languages (not just 2)
- Add source badge display (NAMUR, IATE, DIN)
- Add confidence score UI
- Show multiple definitions (one per source)

**Code Example**:
```typescript
// ETEx: src/frontend/src/components/MultiSourceCard.tsx
/**
 * Adapted from Glossary APP (2025-10-31)
 * Original: vendor/glossary-app/src/frontend/src/components/BilingualCard.tsx
 * Modifications:
 * - Support 3+ languages (not just 2)
 * - Added source badge display
 * - Added confidence score indicator
 * - Support multiple definitions per term
 */

interface MultiSourceCardProps {
  term: Term;
  sources: Source[];  // NEW
  languages: string[];  // NEW (not just 2)
  onSelect?: (termId: number) => void;
}

export const MultiSourceCard: React.FC<MultiSourceCardProps> = ({ ... }) => {
  // ... implementation adapted from BilingualCard ...
};
```

---

#### SearchBar Component (Tier 1 - Use As-Is) 🔍

**Location**: `vendor/glossary-app/src/frontend/src/components/SearchBar.tsx`

**Status**: Excellent

**Quality**: EXCELLENT
- Multiple search modes (simple/phrase/boolean/wildcard)
- Keyboard navigation
- Autocomplete
- Clean Material-UI design

**Reuse Strategy**: **Import directly or copy as-is** (Tier 1)

**Note**: May need Tier 2 adaptation if ETEx search has unique requirements (e.g., source filtering)

**Code Example** (if importing directly):
```typescript
// ETEx: src/frontend/src/pages/SearchPage.tsx
import { SearchBar } from 'vendor/glossary-app/src/frontend/src/components/SearchBar';

export const SearchPage: React.FC = () => {
  return (
    <div>
      <SearchBar
        onSearch={handleSearch}
        placeholder="Search terms across all sources..."
      />
      {/* Rest of page */}
    </div>
  );
};
```

---

#### ThemeContext (Tier 1 - Use As-Is) 🌗

**Location**: `vendor/glossary-app/src/frontend/src/contexts/ThemeContext.tsx`

**Status**: Excellent

**Quality**: Production-ready dark mode implementation

**Reuse Strategy**: **Import directly** (Tier 1)

**Code Example**:
```typescript
// ETEx: src/frontend/src/App.tsx
import { ThemeProvider } from 'vendor/glossary-app/src/frontend/src/contexts/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      {/* App content */}
    </ThemeProvider>
  );
}
```

---

## Reuse Checklist

Before writing new code, check this list:

### Backend
- [ ] PDF extraction? → Use `pdf_extractor.py` (Tier 1)
- [ ] Text cleaning? → Copy utilities from `term_extractor.py` (Tier 2)
- [ ] Translation (Phase 2)? → Use `deepl_client.py` (Tier 1)
- [ ] Database models? → Reference `base_models.py` for schema ideas (Tier 3)
- [ ] File upload? → Check `documents.py` router for patterns (Tier 3)

### Frontend
- [ ] Search UI? → Use `SearchBar.tsx` (Tier 1)
- [ ] Term display? → Adapt `BilingualCard.tsx` (Tier 2)
- [ ] Dark mode? → Use `ThemeContext.tsx` (Tier 1)
- [ ] Document upload? → Check `DocumentUpload.tsx` for patterns (Tier 3)

---

## Sync Vendor Code

**How to update Glossary APP reference**:

```bash
# Pull latest changes from Glossary APP
git submodule update --remote vendor/glossary-app

# Review changes
cd vendor/glossary-app
git log --oneline -5

# If updates look good, commit the submodule update
cd ../..
git add vendor/glossary-app
git commit -m "chore: Update Glossary APP reference to latest

- Bug fixes in pdf_extractor.py
- Performance improvements in search"
```

**Frequency**: Monthly or when Glossary APP has relevant updates

---

## Contributing Back

**If you fix bugs in Tier 1 components**:

Since you can't modify vendor code directly, you have two options:

1. **Create wrapper** with bug fix:
   ```python
   from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor as VendorPDFExtractor

   class PDFExtractor(VendorPDFExtractor):
       def extract(self, pdf_path):
           # Apply bug fix
           result = super().extract(pdf_path)
           # ... fix logic ...
           return result
   ```

2. **Contribute fix back to Glossary APP**:
   - Fork Glossary APP
   - Fix bug
   - Submit pull request
   - Once merged, update submodule

**Recommended**: Option 2 (contribute back) - benefits both projects

---

## Tracking Reused Code

**Maintain in CHANGELOG.md**:

```markdown
## Code Reused from Glossary APP

### Tier 1 - Direct Imports
- pdf_extractor.py (v1.0, 2025-10-31) - PDF extraction
- deepl_client.py (v1.0, 2025-11-15) - Translation API

### Tier 2 - Adapted Components
- term_extractor.py utilities (2025-10-31) - clean_term(), strip_leading_articles()
- BilingualCard.tsx → MultiSourceCard.tsx (2025-11-01) - Adapted for 3+ languages

### Tier 3 - Inspired By
- base_models.py - Database schema reference
- SearchBar.tsx patterns - Search UX inspiration
```

---

## Questions & Answers

**Q: What if vendor code has a bug?**
A:
1. For Tier 1 (imports): Create wrapper with fix, contribute back to Glossary APP
2. For Tier 2 (copies): Fix in your copy, document in attribution header

**Q: What if I modify Tier 1 imported code?**
A: You can't modify vendor directly. Options:
   - Wrapper class that extends vendor class
   - Convert to Tier 2 (copy with attribution)

**Q: How often should I sync vendor/?**
A: Monthly, or when Glossary APP has updates relevant to ETEx

**Q: Can I delete vendor/ to save space?**
A: Not recommended. It's your reference and some code imports from it directly.

**Q: What if Glossary APP changes API?**
A:
   - Tier 1 imports may break (reason to be cautious with Tier 1)
   - Tier 2 copies are isolated (you control them)
   - Consider version pinning the submodule

---

**Last Updated**: 2025-10-31
**Maintained By**: ETEx Development Team
