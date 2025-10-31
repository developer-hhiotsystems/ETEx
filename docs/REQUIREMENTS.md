# ETEx (Engineering Terminology Explorer) - Requirements Document

**Date**: 2025-10-31
**Status**: Requirements Complete - Ready for Implementation
**MVP Target**: 6-week development cycle

---

## 1. Project Overview

### Project Name
**ETEx** - Engineering Terminology Explorer

### Core Purpose
Multi-language terminology search and translation system across industry standards, focusing on:
- Solving German terminology inconsistency problems
- Matching terminology across regional standards (NAMUR ↔ IATE ↔ DIN)
- Building language-internal thesaurus for synonym management
- Providing authoritative terminology sources for engineers, translators, and technical writers

### Primary Problem Being Solved
**German source documents use inconsistent terminology** (e.g., "Drucksensor" vs "Druckmessumformer" vs "Druckaufnehmer"), leading to:
- Confusion within German documentation
- Mistranslations into other languages (English, Spanish, Czech, etc.)
- Difficulty matching terms across different regional standards

**Solution**: Build a language-internal thesaurus that maps synonyms within each language, and match terminology across regional/international standards.

---

## 2. User Profile

### Primary Users
**All user types** will use ETEx:
- Engineers (reviewing technical specs)
- Technical Writers (creating documentation)
- Translators (translating documents)
- Quality Assurance (checking terminology consistency)
- Management (understanding technical concepts)

### User Needs
- **Engineers**: Quick terminology lookups across standards
- **Writers**: Consistent term usage across documents
- **Translators**: Authoritative translations with context
- **QA**: Deviation detection from approved terminology
- **Management**: Understanding technical concepts across languages

---

## 3. Language Requirements

### Must-Have Languages (MVP)
- **German** (primary - must check first)
- **English** (primary)

### Future Languages (Post-MVP)
- Spanish
- Czech
- Chinese
- Korean
- Japanese
- Hindi

**Priority**: German/English foundation must be solid before adding other languages.

---

## 4. Three-Tier Source Priority System

### Tier 1: Authoritative Terms
**Highest priority** - Industry standards and official terminology databases:
- **IATE** (EU Inter-Agency Terminology)
- **NAMUR** (Process Automation Industry)
- **DIN** (German Institute for Standardization)
- **ASME** (American Society of Mechanical Engineers)
- **ISO** (International Organization for Standardization)
- **IEC Electropedia** (International Electrotechnical Commission)

### Tier 2: Translators & Lexica
**Medium priority** - Professional translation resources:
- DeepL translations
- Professional lexicons
- Translation memory systems

### Tier 3: Internal Terms
**Lowest priority** - Organization-specific terminology:
- Company glossaries
- Project-specific terms
- Internal documentation terminology

### Key Design Principle
**NO automatic bias toward any single standard**. ETEx shows:
- Where each term comes from (source transparency)
- How different standards define the same concept
- User decides which source to trust for their context

**The system is flexible** - authoritative sources can be added or removed dynamically through pluggable "Authoritative Modules".

---

## 5. Authoritative Module Architecture

### Concept
Each authoritative source (IATE, NAMUR, DIN, etc.) is implemented as a **pluggable module** that can:
- Be added/removed independently
- Have its own import/update mechanism
- Define its own metadata structure
- Be enabled/disabled per user/organization

### Module Types

#### Type A: API-Based Modules
- Connect to external terminology APIs
- Real-time or cached lookups
- Example: IATE API, commercial terminology services

#### Type B: PDF Upload Modules
- Extract terms + definitions from authoritative PDFs
- Store page references for citation
- Example: NAMUR standards, DIN standards

#### Type C: Database Import Modules
- Import from structured formats (TBX, CSV, Excel)
- One-time or periodic updates
- Example: IEC Electropedia exports, ISO terminology databases

#### Type D: Manual Entry Modules
- Web interface for manual term entry
- Quality review workflow
- Example: Internal glossary curation

---

## 6. Language-Internal Thesaurus

### Purpose
Map **synonyms within the same language** to solve German terminology inconsistency problem.

### Example Use Case
German synonyms for "pressure sensor":
- "Drucksensor"
- "Druckmessumformer"
- "Druckaufnehmer"
- "Druckgeber"

ETEx recognizes these as synonyms and:
- Shows all variants when searching
- Maps how different standards use different terms
- **Does NOT automatically prefer one** (user chooses based on context)

### Synonym Detection
- **Auto-detection**: System detects potential synonyms using:
  - Co-occurrence in translations across standards
  - Similar definitions with high semantic overlap
  - User search patterns
- **User review**: Auto-detected synonyms require user approval
- **Confidence scoring**: Each synonym link has confidence score

### Preferred Term (Optional)
- Users **may** define a preferred term within a thesaurus group
- This is for **organizational preference**, not a system-wide default
- Example: Company policy says "use 'Drucksensor' not 'Druckaufnehmer'"

---

## 7. Multi-Regional Terminology Matching

### Purpose
**Compare how different standards define the same concept** across regions/disciplines.

### Example Query: "pressure transmitter"
ETEx shows:
```
English: "pressure transmitter"

NAMUR (Process Automation):
  German: "Druckmessumformer"
  Definition: "Device converting pressure to standardized signal"
  Context: Process instrumentation

IATE (EU Standards):
  German: "Druckgeber"
  Definition: "Pressure measurement device"
  Context: General engineering

DIN 16086:
  German: "Drucksensor"
  Definition: "Sensor for pressure measurement"
  Context: Measurement technology

IEC Electropedia:
  German: "Druckaufnehmer"
  Definition: "Transducer for pressure signals"
  Context: Electrical engineering
```

**User sees**:
- All regional/disciplinary variants
- Source of each definition
- Context where each term is preferred
- **User decides** which term to use based on their document context

---

## 8. Document Processing Workflows

### Workflow A: Import Authoritative PDF
1. User uploads NAMUR standard PDF (e.g., NE107)
2. System extracts terms + definitions using `pdf_extractor.py`
3. System runs NLP term extraction (`term_extractor.py`)
4. User reviews extracted terms
5. User approves → terms stored with source metadata
6. Terms become searchable in ETEx

### Workflow B: Import from API (IATE)
1. System connects to IATE API
2. Queries for domain-specific terminology (e.g., "process automation")
3. Imports terms + translations + definitions
4. Stores with IATE source metadata
5. Periodic sync updates

### Workflow C: Database Import (IEC Electropedia)
1. User imports IEC database export (22,798 terms @ 92.4% German coverage)
2. System parses TBX/CSV format
3. Maps to ETEx schema
4. Stores with IEC source metadata
5. Terms become searchable

### Workflow D: Manual Entry
1. User searches term, not found
2. User clicks "Add to glossary"
3. Enters term, definition, translation, source
4. Optional: Mark as "Internal term" (Tier 3)
5. Stores for organization-wide use

---

## 9. Search & Browse Interface

### Search is THE Most Important Feature
**User Quote**: "This cant be answered because different purpose of using this tool - all are important"

Translation: **All search result information is important** - the system must show:
- Term in all available languages
- Definition from each source
- Source metadata (NAMUR, IATE, DIN, etc.)
- Context information (domain, discipline)
- Synonym relationships
- Confidence scores

### Search Modes (Reuse from Current Project)
- **Simple search**: Basic term lookup
- **Phrase search**: Multi-word terms
- **Boolean search**: AND/OR/NOT operators
- **Wildcard search**: Partial term matching

### Browse Modes
- Browse by source (IATE, NAMUR, DIN, etc.)
- Browse by domain (process automation, electrical engineering, etc.)
- Browse by language
- Browse by thesaurus groups (synonyms)

### Result Display
Reuse `BilingualCard.tsx` component with enhancements:
- Show source badge (NAMUR, IATE, etc.)
- Show confidence score
- Show synonym links
- Show definition from each source (if multiple)
- Side-by-side multi-language display

---

## 10. MVP Scope Definition

### ✅ MVP Includes (Phase 1: 6 weeks)

**Focus**: Build robust authoritative source interface FIRST

#### 1. Authoritative Module System
- Pluggable architecture for adding sources
- Module registration/activation system
- Source metadata tracking

#### 2. Multiple Input Methods
- **API Integration**: IATE API module (Type A)
- **PDF Upload**: NAMUR/DIN PDF processing (Type B)
- **Database Import**: IEC Electropedia import (Type C)
- **Manual Entry**: Web interface (Type D)

#### 3. Robust Processing
- Parse different formats reliably (PDF, TBX, CSV, API responses)
- Extract terms + definitions + metadata
- Handle errors gracefully (malformed PDFs, API timeouts)
- Track source provenance (who added what when)
- Validation & quality checks

#### 4. Core Database Schema
- `AuthoritativeSource` table
- `Term` table (multi-language)
- `TermSynonym` table (thesaurus)
- `Translation` table (cross-language mappings)
- `UploadedDocument` table

#### 5. Search & Browse Interface
- Basic search (simple, phrase, boolean)
- Browse by source
- Browse by language
- Result display with source metadata
- Reuse `SearchBar.tsx` and `BilingualCard.tsx`

#### 6. Language Support
- German (primary)
- English (primary)
- Database structure supports future languages

### ❌ MVP Excludes (Phase 2: Later)

#### Deferred to Phase 2
- **Internal document processing** (company docs, project files)
- **Deviation checking** (compare doc terms vs approved glossary)
- **DeepL integration** (Tier 2 translations)
- **Additional languages** (Spanish, Czech, Chinese, etc.)
- **User accounts & permissions**
- **Synonym auto-detection** (manual synonym linking in MVP)
- **Advanced thesaurus features** (preferred terms, confidence scoring)
- **Batch operations** (bulk imports, bulk edits)

---

## 11. Technology Stack

### Backend
- **Python 3.12+**
- **FastAPI** (web framework)
- **SQLAlchemy** (ORM)
- **SQLite** (database - development server)
- **Alembic** (migrations)
- **spaCy** (NLP - term extraction)

### Frontend
- **React 18+**
- **Material-UI (MUI)** (component library)
- **Vite** (build tool)

### Deployment
- **Development server** initially
- **Production deployment** if POC successful

### Why Keep Same Stack?
**User Choice**: "a) Keep same tech stack"

**Reasoning**:
- Current stack is proven and working
- Team familiar with Python/FastAPI/React
- Can reuse significant code from current Glossary Management System
- SQLite sufficient for MVP (can scale to PostgreSQL later)

---

## 12. Reusable Components from Current Project

### Backend Components

#### ✅ `src/backend/services/pdf_extractor.py`
**Quality**: EXCELLENT - Production-ready
**Reuse Decision**: Use as-is, zero modifications
**Features**:
- Page-by-page PDF extraction
- OCR normalization (handles encoding errors)
- 100+ test cases validated

#### ✅ `src/backend/services/term_extractor.py`
**Quality**: GOOD with caveats
**Reuse Decision**: Extract utilities (clean_term, strip_leading_articles)
**Features**:
- Multi-language support (EN/DE)
- Article stripping ("the", "der", "die", "das")
- Frequency-based filtering
- Confidence scoring

#### ✅ `src/backend/base_models.py`
**Quality**: EXCELLENT
**Reuse Decision**: Adapt for new schema
**Key Models**:
- `GlossaryEntry` → adapt to `Term`
- `TranslationHistory` → adapt to `Translation`
- `TermDocumentReference` → reuse for PDF page references

#### ⚠️ `src/backend/services/translation/clients/deepl_client.py`
**Quality**: GOOD
**Reuse Decision**: Phase 2 only (Tier 2 translations)
**Features**:
- DeepL API integration
- Batch translation
- Glossary support
- Usage tracking

### Frontend Components

#### ✅ `src/frontend/src/components/BilingualCard.tsx`
**Quality**: EXCELLENT
**Reuse Decision**: Adapt for multi-source display
**Features**:
- Side-by-side EN/DE display
- Synchronized scrolling
- Language toggle
- Selection checkboxes

#### ✅ `src/frontend/src/components/SearchBar.tsx`
**Quality**: EXCELLENT
**Reuse Decision**: Use as-is
**Features**:
- Multiple search modes (simple/phrase/boolean/wildcard)
- Keyboard navigation
- Autocomplete

---

## 13. Database Schema (MVP)

### Core Tables

#### `authoritative_sources`
```sql
CREATE TABLE authoritative_sources (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,           -- "IATE", "NAMUR", "DIN"
    display_name TEXT NOT NULL,          -- "IATE - EU Terminology"
    source_type TEXT NOT NULL,           -- "api", "pdf", "database", "manual"
    tier INTEGER DEFAULT 1,              -- 1=Authoritative, 2=Translators, 3=Internal
    is_active BOOLEAN DEFAULT TRUE,
    config_json TEXT,                    -- Module-specific config
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `terms`
```sql
CREATE TABLE terms (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,                  -- The actual term
    language_code TEXT NOT NULL,         -- "en", "de", "es", etc.
    definition TEXT,                     -- Definition in same language
    source_id INTEGER,                   -- FK to authoritative_sources
    document_id INTEGER,                 -- FK to uploaded_documents (if from PDF)
    page_reference TEXT,                 -- Page number in PDF
    gender TEXT,                         -- "m", "f", "n" (for German nouns)
    part_of_speech TEXT,                 -- "noun", "verb", "adjective"
    context TEXT,                        -- Domain/discipline context
    preferred_term_id INTEGER,           -- FK to terms (for thesaurus)
    confidence REAL DEFAULT 1.0,         -- 0.0-1.0 confidence score
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES authoritative_sources(id),
    FOREIGN KEY (document_id) REFERENCES uploaded_documents(id),
    FOREIGN KEY (preferred_term_id) REFERENCES terms(id),
    INDEX idx_term_language (term, language_code),
    INDEX idx_source (source_id),
    INDEX idx_language (language_code)
);
```

#### `term_synonyms`
```sql
CREATE TABLE term_synonyms (
    id INTEGER PRIMARY KEY,
    term_id_1 INTEGER NOT NULL,          -- FK to terms
    term_id_2 INTEGER NOT NULL,          -- FK to terms
    confidence REAL DEFAULT 1.0,         -- 0.0-1.0 synonym confidence
    is_approved BOOLEAN DEFAULT FALSE,   -- Manual review flag
    detection_method TEXT,               -- "auto", "manual", "co-occurrence"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by TEXT,                    -- User who approved (Phase 2)
    approved_at TIMESTAMP,
    FOREIGN KEY (term_id_1) REFERENCES terms(id),
    FOREIGN KEY (term_id_2) REFERENCES terms(id),
    CHECK (term_id_1 < term_id_2),       -- Prevent duplicates
    UNIQUE (term_id_1, term_id_2)
);
```

#### `translations`
```sql
CREATE TABLE translations (
    id INTEGER PRIMARY KEY,
    source_term_id INTEGER NOT NULL,     -- FK to terms
    target_term_id INTEGER NOT NULL,     -- FK to terms
    source_language TEXT NOT NULL,       -- "en", "de", etc.
    target_language TEXT NOT NULL,       -- "de", "en", etc.
    authoritative_source_id INTEGER,     -- FK to authoritative_sources
    confidence REAL DEFAULT 1.0,         -- 0.0-1.0 translation confidence
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_term_id) REFERENCES terms(id),
    FOREIGN KEY (target_term_id) REFERENCES terms(id),
    FOREIGN KEY (authoritative_source_id) REFERENCES authoritative_sources(id),
    INDEX idx_source_target (source_term_id, target_term_id),
    INDEX idx_languages (source_language, target_language)
);
```

#### `uploaded_documents`
```sql
CREATE TABLE uploaded_documents (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    file_path TEXT NOT NULL,             -- Storage location
    file_size INTEGER,
    file_type TEXT,                      -- "pdf", "csv", "tbx"
    source_id INTEGER,                   -- FK to authoritative_sources
    upload_status TEXT DEFAULT 'pending', -- "pending", "processing", "completed", "failed"
    processing_log TEXT,                 -- Error messages, warnings
    terms_extracted INTEGER DEFAULT 0,   -- Count of terms extracted
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES authoritative_sources(id)
);
```

---

## 14. API Endpoints (MVP)

### Authoritative Sources
- `GET /api/sources` - List all authoritative sources
- `POST /api/sources` - Add new authoritative source
- `PUT /api/sources/{id}` - Update source configuration
- `DELETE /api/sources/{id}` - Deactivate source
- `GET /api/sources/{id}/stats` - Get source statistics

### Document Upload & Processing
- `POST /api/documents/upload` - Upload PDF/CSV/TBX
- `GET /api/documents/{id}` - Get document details
- `POST /api/documents/{id}/process` - Trigger term extraction
- `GET /api/documents/{id}/terms` - Get extracted terms
- `DELETE /api/documents/{id}` - Delete document

### Terms
- `GET /api/terms` - Search/browse terms (with filters)
- `POST /api/terms` - Add term manually
- `GET /api/terms/{id}` - Get term details
- `PUT /api/terms/{id}` - Update term
- `DELETE /api/terms/{id}` - Delete term
- `GET /api/terms/{id}/synonyms` - Get synonyms
- `GET /api/terms/{id}/translations` - Get translations

### Synonyms
- `POST /api/synonyms` - Link two terms as synonyms
- `DELETE /api/synonyms/{id}` - Remove synonym link
- `PUT /api/synonyms/{id}/approve` - Approve auto-detected synonym

### Translations
- `GET /api/translations` - Get translations for term
- `POST /api/translations` - Add translation manually

### Import
- `POST /api/import/iate` - Trigger IATE import
- `POST /api/import/iec` - Import IEC database
- `GET /api/import/{job_id}` - Get import job status

---

## 15. Success Criteria

### MVP Success = Authoritative Interface Works Robustly

#### Functional Requirements
✅ Can import IATE terms via API
✅ Can upload NAMUR PDF and extract terms
✅ Can import IEC Electropedia database (22,798 terms)
✅ Can manually add terms via web interface
✅ Can search terms across all sources
✅ Can browse terms by source
✅ Can view term details with source metadata
✅ Can link synonyms manually
✅ System handles errors gracefully (malformed PDFs, API failures)

#### Quality Requirements
✅ PDF extraction accuracy > 95% (reuse existing `pdf_extractor.py`)
✅ API import completes without crashes
✅ Database import handles 20,000+ terms
✅ Search responds in < 500ms
✅ UI is responsive and intuitive

#### Technical Requirements
✅ Database schema supports future languages
✅ Authoritative module architecture is extensible
✅ Code is well-documented
✅ Error logging is comprehensive

### Post-MVP Success (Phase 2)
- Internal document processing works
- Deviation checking identifies terminology inconsistencies
- DeepL integration provides Tier 2 translations
- Spanish, Czech, Chinese support added
- Synonym auto-detection achieves >80% accuracy

---

## 16. Implementation Plan (6-Week MVP)

### Week 1: Project Setup & Database
**Goal**: Foundation in place

**Tasks**:
- Create new ETEx project directory
- Initialize FastAPI backend with Alembic migrations
- Create database schema (5 core tables)
- Initialize React frontend with Vite + MUI
- Copy reusable components from current project
- Set up dev environment

**Deliverable**: Empty app with database schema and dev server running

---

### Week 2: Document Upload & PDF Processing
**Goal**: PDF upload works end-to-end

**Tasks**:
- Build `uploaded_documents` CRUD API
- Integrate `pdf_extractor.py` for PDF processing
- Create file upload UI component
- Create document list/detail views
- Test with NAMUR PDF sample
- Error handling for malformed PDFs

**Deliverable**: Can upload PDF, extract text page-by-page, view results

---

### Week 3: Term Extraction & Storage
**Goal**: Terms extracted from PDFs are stored in database

**Tasks**:
- Integrate `term_extractor.py` for NLP extraction
- Build term review UI (approve/reject extracted terms)
- Create `terms` CRUD API
- Create term detail view component
- Test with NAMUR NE107 standard
- Store source metadata (document, page reference)

**Deliverable**: Can extract terms from PDF, review, approve, store in DB

---

### Week 4: IATE API Integration
**Goal**: IATE import works

**Tasks**:
- Research IATE API documentation
- Build IATE authoritative module (Type A)
- Create import job system (background processing)
- Build import UI (trigger, monitor progress)
- Store IATE terms with source metadata
- Test with "process automation" domain

**Deliverable**: Can import IATE terms via API, view in ETEx

---

### Week 5: IEC Database Import & Search
**Goal**: IEC data imported, search works

**Tasks**:
- Build IEC import module (Type C - CSV/TBX parser)
- Import 22,798 IEC terms (92.4% German coverage)
- Build search API with filters (source, language, term)
- Create search UI (reuse `SearchBar.tsx`)
- Create results display (adapt `BilingualCard.tsx`)
- Test search performance with 20,000+ terms

**Deliverable**: Can import IEC database, search terms across sources

---

### Week 6: Manual Entry, Browse & Polish
**Goal**: MVP feature-complete

**Tasks**:
- Build manual term entry UI (Type D module)
- Build browse-by-source UI
- Build browse-by-language UI
- Manual synonym linking UI
- Error handling & validation polish
- Documentation (README, API docs)
- Testing & bug fixes

**Deliverable**: Functional MVP ready for POC demonstration

---

## 17. Post-MVP Roadmap (Phase 2)

### Phase 2A: Internal Document Processing (2-3 weeks)
- Upload internal company documents
- Extract terminology from internal docs
- Mark as Tier 3 (Internal) source
- Compare internal vs authoritative terms

### Phase 2B: Deviation Checking (2-3 weeks)
- Upload document to check
- Extract terms from document
- Compare vs approved glossary (Tier 1/2)
- Highlight deviations
- Suggest replacements

### Phase 2C: DeepL Integration (1-2 weeks)
- Integrate `deepl_client.py`
- Add DeepL as Tier 2 source
- Fallback translation if authoritative not found
- Glossary support for consistent translations

### Phase 2D: Additional Languages (2-3 weeks)
- Spanish support
- Czech support
- Chinese support
- Korean, Japanese, Hindi (lower priority)

### Phase 2E: Synonym Auto-Detection (2-3 weeks)
- Co-occurrence analysis
- Semantic similarity (word embeddings)
- User review workflow for auto-detected synonyms
- Confidence scoring

### Phase 2F: User Accounts & Permissions (2-3 weeks)
- User authentication
- Role-based access (admin, editor, viewer)
- Track who added/edited terms
- Organization-level glossaries

---

## 18. Known Constraints & Assumptions

### Constraints
- **Budget**: Development server only initially (no cloud deployment costs)
- **Team**: Assuming small team (1-3 developers)
- **Time**: 6-week MVP timeline is aggressive but achievable
- **Data**: Dependent on IATE API availability, NAMUR PDF quality

### Assumptions
- IATE API is publicly accessible and documented
- NAMUR PDFs are text-based (not scanned images)
- IEC Electropedia database export is available (already confirmed: 22,798 terms @ 92.4% German)
- Current project's `pdf_extractor.py` works without modifications
- SQLite sufficient for MVP (20,000-50,000 terms)

### Risks
- **IATE API changes**: Mitigation - abstract API calls behind module interface
- **PDF extraction accuracy**: Mitigation - reuse proven `pdf_extractor.py` (100+ test cases)
- **Search performance**: Mitigation - database indexing, consider full-text search (FTS5) if needed
- **Scope creep**: Mitigation - strict MVP definition, defer Phase 2 features

---

## 19. Questions for User (Future Clarifications)

These can wait until implementation begins:

1. **IATE API Access**: Do you have IATE API credentials, or is it public?
2. **NAMUR Standards**: Which specific NAMUR standards do you want to import first?
3. **DIN Standards**: Do you have access to DIN PDF standards, or is this future work?
4. **IEC Data**: You mentioned IEC Electropedia with 92.4% German coverage - is this database already available?
5. **Deployment**: "Development server" - does this mean localhost, or a shared dev server?
6. **Branding**: Any specific colors, logos, or branding for ETEx UI?

---

## 20. Final Notes

### Why This Approach?
The step-by-step requirements gathering revealed the **real problem**: German terminology inconsistency causing downstream translation errors. The solution is **not just a glossary app**, but a **terminology intelligence system** that:

1. Aggregates authoritative sources (multi-regional)
2. Maps synonyms within languages (thesaurus)
3. Matches terms across standards (NAMUR ↔ IATE ↔ DIN)
4. Provides transparency (source metadata always visible)
5. Empowers users to make context-appropriate choices

### MVP Philosophy
**Build the authoritative interface FIRST** because:
- It's the foundation for everything else
- It's the hardest part to get right (multiple formats, error handling)
- Internal docs and deviation checking are useless without authoritative baseline
- POC can demonstrate value with just authoritative sources

### Next Steps
1. **Review this document** - confirm requirements match your vision
2. **Clarify any questions** - especially about data sources (IATE, IEC, DIN access)
3. **Begin implementation** - start Week 1 (project setup & database)

---

**Document Status**: ✅ Complete
**Ready for**: Implementation (Week 1 kickoff)
**Last Updated**: 2025-10-31

