# Create Week 1 Issues - Manual Guide

**Purpose**: Create GitHub issues for Week 1 tasks manually (since gh CLI not installed)
**Last Updated**: 2025-10-31

---

## Option 1: Install GitHub CLI (Recommended)

### Install `gh` CLI on Windows

**Download**: https://cli.github.com/

**Or use winget**:
```powershell
winget install --id GitHub.cli
```

**Or use Chocolatey**:
```powershell
choco install gh
```

**After install**:
```bash
gh auth login
# Follow prompts to authenticate
```

---

## Option 2: Create Issues via Web Interface

### Issue #1: Database Schema (Week 1)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=feature_request.yml

**Fill in the form**:

**Title**:
```
feat(backend): Create database schema with SQLAlchemy models (Week 1)
```

**Component**: Backend (Python/FastAPI)

**Phase**: MVP (6 weeks)

**Priority**: High (important for current week)

**Feature Overview**:
```
Implement the 5 core database tables using SQLAlchemy ORM as defined in docs/REQUIREMENTS.md section 13.
```

**Acceptance Criteria**:
```
- [ ] authoritative_sources table (12 fields: id, name, display_name, source_type, tier, is_active, config_json, created_at, updated_at)
- [ ] terms table (14 fields: id, term, language_code, definition, source_id, document_id, page_reference, gender, pos, context, confidence, timestamps)
- [ ] term_synonyms table (bidirectional relationship, confidence scoring)
- [ ] translations table (source/target language validation, confidence)
- [ ] uploaded_documents table (file tracking, processing status)
- [ ] All foreign keys with proper CASCADE behavior
- [ ] Indexes for performance (source_id, language_code, term full-text search)
- [ ] Timestamps (created_at, updated_at) auto-managed
```

**Related Specification**:
```
docs/REQUIREMENTS.md section 13 (Database Schema)
```

**Implementation Notes**:
```
- Reference vendor/glossary-app/src/backend/base_models.py for pattern (Tier 3)
- Use SQLAlchemy 2.0+ syntax
- Store database at data/database/etex.db (gitignored)
- Create models in src/backend/models/
- Each model in separate file (authoritative_source.py, term.py, etc.)

Technical Details:
- authoritative_sources: id, name, display_name, source_type (enum), tier (1-3), is_active, config_json
- terms: id, term, language_code, definition, source_id, document_id, page_reference, gender, pos, context, confidence
- term_synonyms: id, term_id_1, term_id_2, confidence, is_approved, detection_method
- translations: id, source_term_id, target_term_id, source_lang, target_lang, confidence
- uploaded_documents: id, filename, file_path, file_type, source_id, upload_status, processing_log

Indexes:
- idx_terms_language on (language_code)
- idx_terms_source on (source_id)
- idx_translations_source_lang on (source_lang, target_lang)
- FTS5 full-text search on (term, definition)
```

**Week / Sprint**:
```
Week 1
```

**Dependencies**:
```
None (first task)
Blocks: Alembic migrations, Week 2 API endpoints
```

**Estimated Effort**: 🔶 Large (1-2 days)

**Click "Submit new issue"**

---

### Issue #2: Alembic Migrations (Week 1)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=feature_request.yml

**Title**:
```
feat(backend): Setup Alembic database migrations (Week 1)
```

**Component**: Backend (Python/FastAPI)

**Phase**: MVP (6 weeks)

**Priority**: High (important for current week)

**Feature Overview**:
```
Setup Alembic for database schema versioning and migrations.
```

**Acceptance Criteria**:
```
- [ ] alembic.ini configured with SQLite database URL
- [ ] alembic/env.py setup with ETEx models import
- [ ] Initial migration created (001_initial_schema.py)
- [ ] Migration runs successfully (alembic upgrade head)
- [ ] Database created at data/database/etex.db
- [ ] Rollback works (alembic downgrade base)
- [ ] Migration script includes all 5 tables
- [ ] All indexes and foreign keys included
```

**Related Specification**:
```
docs/REQUIREMENTS.md section 11 (Technology Stack - Alembic)
```

**Implementation Notes**:
```
- Follow Alembic best practices
- Auto-generate migration from models: alembic revision --autogenerate -m "Initial schema"
- Test upgrade/downgrade cycle
- Document migration commands in docs/getting-started/SETUP.md

Commands:
alembic init alembic
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
alembic downgrade base
```

**Week / Sprint**:
```
Week 1
```

**Dependencies**:
```
Depends on: Issue #1 (database schema must exist first)
Blocks: Week 2 development (need migrations working)
```

**Estimated Effort**: 🔹 Small (< 4 hours)

**Click "Submit new issue"**

---

### Issue #3: Pydantic Schemas (Week 1)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=feature_request.yml

**Title**:
```
feat(backend): Create Pydantic schemas for request/response validation (Week 1)
```

**Component**: Backend (Python/FastAPI)

**Phase**: MVP (6 weeks)

**Priority**: High

**Feature Overview**:
```
Create Pydantic schemas for API request/response validation, separate from SQLAlchemy models.
```

**Acceptance Criteria**:
```
- [ ] AuthoritativeSourceCreate schema (POST request)
- [ ] AuthoritativeSourceResponse schema (GET response)
- [ ] AuthoritativeSourceUpdate schema (PUT request)
- [ ] TermCreate, TermResponse, TermUpdate schemas
- [ ] TermSynonymCreate, TermSynonymResponse schemas
- [ ] TranslationCreate, TranslationResponse schemas
- [ ] DocumentUploadResponse schema
- [ ] All schemas have proper validation (required fields, field types)
- [ ] Example values in schema docstrings (for API docs)
```

**Related Specification**:
```
docs/REQUIREMENTS.md section 14 (API Endpoints)
```

**Implementation Notes**:
```
Create in src/backend/schemas.py or src/backend/schemas/ directory

Example schema:
class AuthoritativeSourceCreate(BaseModel):
    name: str = Field(..., max_length=100, example="iate")
    display_name: str = Field(..., max_length=200, example="IATE (EU Terminology)")
    source_type: SourceType = Field(..., example="api")
    tier: int = Field(..., ge=1, le=3, example=1)
    is_active: bool = Field(default=True)
    config_json: Optional[dict] = Field(default=None)

Separate schemas for:
- Create (input validation)
- Update (partial updates allowed)
- Response (output serialization, includes id, timestamps)
```

**Week / Sprint**:
```
Week 1
```

**Dependencies**:
```
Depends on: Issue #1 (models define the structure)
Blocks: API endpoint implementation (Week 2)
```

**Estimated Effort**: 🔸 Medium (4-8 hours)

**Click "Submit new issue"**

---

### Issue #4: Environment Configuration (Week 1)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=feature_request.yml

**Title**:
```
chore(config): Create .env.example and requirements.txt (Week 1)
```

**Component**: Backend (Python/FastAPI)

**Phase**: MVP (6 weeks)

**Priority**: High

**Feature Overview**:
```
Create environment configuration template and Python dependencies file for reproducible setup.
```

**Acceptance Criteria**:
```
- [ ] .env.example created with all required variables
- [ ] requirements.txt with pinned versions
- [ ] requirements-dev.txt for development dependencies
- [ ] Documentation in docs/getting-started/SETUP.md updated
- [ ] .gitignore ensures .env is not committed
```

**Related Specification**:
```
docs/REQUIREMENTS.md section 11 (Technology Stack)
docs/getting-started/SETUP.md (Setup instructions)
```

**Implementation Notes**:
```
.env.example should include:
# Database
DATABASE_URL=sqlite:///data/database/etex.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=9123
API_DEBUG=true

# IATE API (Week 4)
IATE_API_KEY=your_key_here
IATE_API_ENDPOINT=https://iate.europa.eu/api

# DeepL (Phase 2)
DEEPL_API_KEY=your_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/etex.log

requirements.txt should include:
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
pydantic>=2.4.0
python-dotenv>=1.0.0
PyPDF2>=3.0.0  # PDF extraction
spaCy>=3.7.0  # NLP (term extraction)

requirements-dev.txt:
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0
black>=23.10.0
flake8>=6.1.0
```

**Week / Sprint**:
```
Week 1
```

**Dependencies**:
```
None (can be done in parallel)
```

**Estimated Effort**: 🔹 Small (< 4 hours)

**Click "Submit new issue"**

---

### Issue #5: React Frontend Scaffold (Week 1)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/issues/new?template=feature_request.yml

**Title**:
```
feat(frontend): Initialize React frontend with Vite and Material-UI (Week 1)
```

**Component**: Frontend (React/TypeScript)

**Phase**: MVP (6 weeks)

**Priority**: Medium

**Feature Overview**:
```
Setup React 18 frontend with Vite, TypeScript, and Material-UI component library.
```

**Acceptance Criteria**:
```
- [ ] Vite project initialized in src/frontend/
- [ ] TypeScript configured (tsconfig.json)
- [ ] Material-UI (MUI) installed and configured
- [ ] Basic app structure (App.tsx, main.tsx, routes)
- [ ] Dark/light theme toggle (copy ThemeContext from vendor)
- [ ] Development server runs on port 5173
- [ ] Proxy configured to backend API (port 9123)
- [ ] package.json with all dependencies
```

**Related Specification**:
```
docs/REQUIREMENTS.md section 11 (Technology Stack - Frontend)
docs/reference/code-reuse-strategy.md (ThemeContext reuse)
```

**Implementation Notes**:
```
Initialize Vite:
cd src/frontend
npm create vite@latest . -- --template react-ts
npm install

Install MUI:
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled

Reuse from vendor (Tier 1):
- Copy vendor/glossary-app/src/frontend/src/contexts/ThemeContext.tsx
- Copy vendor/glossary-app/src/frontend/src/components/theme/ (if exists)

Project structure:
src/frontend/
├── public/          # Static assets
├── src/
│   ├── components/  # React components
│   ├── pages/       # Page components
│   ├── contexts/    # React contexts (theme, etc.)
│   ├── App.tsx      # Main app component
│   └── main.tsx     # Entry point
├── package.json
├── vite.config.ts
└── tsconfig.json

Vite proxy config (vite.config.ts):
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:9123',
        changeOrigin: true
      }
    }
  }
})
```

**Week / Sprint**:
```
Week 1
```

**Dependencies**:
```
None (can be done in parallel with backend)
```

**Estimated Effort**: 🔸 Medium (4-8 hours)

**Click "Submit new issue"**

---

### Issue #6: Week 1 Meta-Issue (Tracker)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/issues/new

**Title**:
```
meta: Week 1 - Project Setup & Database (Milestone Tracker)
```

**Description**:
```markdown
## Week 1 Goals (Oct 31 - Nov 7)

**Objective**: Setup development environment, create database schema, initialize frontend

### Tasks
- [ ] #1 - Create database schema with SQLAlchemy models
- [ ] #2 - Setup Alembic migrations
- [ ] #3 - Create Pydantic schemas for API validation
- [ ] #4 - Create .env.example and requirements.txt
- [ ] #5 - Initialize React frontend with Vite and Material-UI

### Success Criteria
- All 5 database tables created and migrated
- Development environment fully functional (backend + frontend run locally)
- Tests passing (80%+ coverage)
- Documentation updated
- Ready for Week 2 (PDF upload implementation)

### Week 1 Deliverables
- [ ] SQLAlchemy models for 5 core tables
- [ ] Alembic migration scripts working (upgrade/downgrade)
- [ ] Pydantic schemas for all endpoints
- [ ] .env.example and requirements.txt complete
- [ ] React app running on localhost:5173
- [ ] Backend API running on localhost:9123
- [ ] Unit tests for models (80%+ coverage)
- [ ] Git commit: "Week 1 complete"

### Estimated Timeline
- Days 1-2: Database schema + Alembic (#1, #2)
- Day 3: Pydantic schemas + config (#3, #4)
- Days 4-5: React frontend setup (#5)
- Day 6-7: Testing, documentation, cleanup

### Blockers
None (Week 1 is foundation)

### Progress
0% complete (0/5 tasks done)
```

**Labels**: `type: meta`, `phase: mvp`, `priority: high`

**Click "Submit new issue"**

---

## After Creating Issues

### 1. Create Milestone (Optional)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/milestones/new

**Title**: `Week 1: Project Setup & Database`

**Due date**: `2025-11-07` (7 days from Oct 31)

**Description**: Foundation for ETEx MVP - database schema, environment setup, frontend scaffold

**Assign issues #1-5 to this milestone**

---

### 2. Create Project Board (Optional)

**Go to**: https://github.com/developer-hhiotsystems/ETEx/projects/new

**Name**: `ETEx MVP - 6 Week Sprint`

**Template**: Board

**Columns**: Backlog, Ready, In Progress, Review, Done

**Add all issues to the board**

---

## Quick Reference: Issue URLs

Once created, issues will be at:
- Issue #1: https://github.com/developer-hhiotsystems/ETEx/issues/1
- Issue #2: https://github.com/developer-hhiotsystems/ETEx/issues/2
- Issue #3: https://github.com/developer-hhiotsystems/ETEx/issues/3
- Issue #4: https://github.com/developer-hhiotsystems/ETEx/issues/4
- Issue #5: https://github.com/developer-hhiotsystems/ETEx/issues/5
- Issue #6: https://github.com/developer-hhiotsystems/ETEx/issues/6

---

**End of Week 1 Issue Creation Guide**
**Last Updated**: 2025-10-31
