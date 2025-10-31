# ETEx - Engineering Terminology Explorer

**Status**: 🚧 In Development (MVP Phase)
**Version**: 0.1.0
**Last Updated**: 2025-10-31

---

## What is ETEx?

ETEx (Engineering Terminology Explorer) is a **multi-language terminology search and translation system** across industry standards, focusing on solving German terminology inconsistency problems.

### The Problem We're Solving

German source documents use **inconsistent terminology** (e.g., "Drucksensor" vs "Druckmessumformer" vs "Druckaufnehmer"), leading to:
- Confusion within German documentation
- Mistranslations into other languages
- Difficulty matching terms across different regional standards

### Our Solution

ETEx builds a **language-internal thesaurus** that:
- Maps synonyms within each language
- Matches terminology across regional/international standards (NAMUR ↔ IATE ↔ DIN ↔ IEC)
- Provides authoritative terminology sources with full transparency
- Empowers users to make context-appropriate terminology choices

---

## Quick Start

### Prerequisites

- **Python 3.12+** (backend)
- **Node.js 18+** (frontend)
- **Git** (for vendor code reference)

### Installation

```bash
# 1. Clone repository
cd "C:\Users\developer\Documents\Coding Projects\ETEx"

# 2. Initialize vendor submodule (Glossary APP reference)
git submodule update --init

# 3. Setup Python backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 4. Setup React frontend
cd src/frontend
npm install
cd ../..

# 5. Configure environment
copy .env.example .env
# Edit .env with your API keys and settings

# 6. Run database migrations
cd src/backend
alembic upgrade head
cd ../..
```

### Running Development Servers

**Terminal 1 - Backend**:
```bash
cd src/backend
../../venv/Scripts/uvicorn app:app --host 0.0.0.0 --port 9123 --reload
```

**Terminal 2 - Frontend**:
```bash
cd src/frontend
npm run dev
```

**Access**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:9123
- API Docs: http://localhost:9123/docs

---

## Project Structure

```
ETEx/
├── README.md                      # This file
├── CLAUDE.md                      # AI agent guidelines (role-based)
├── .gitignore                     # Git ignore rules
├── .env.example                   # Environment template
│
├── .agent/                        # 🤖 Agent workspace (temporary)
│   ├── README.md                  # Agent workspace guide
│   ├── workspace/                 # Temporary working files (gitignored)
│   └── outputs/                   # Completed artifacts (committed)
│
├── vendor/                        # 📚 External references
│   └── glossary-app/              # Git submodule (read-only reference)
│
├── docs/                          # 📖 Documentation
│   ├── README.md                  # Documentation index
│   ├── REQUIREMENTS.md            # Complete requirements document
│   ├── architecture/              # System design docs
│   ├── reference/                 # Code reuse guide
│   │   └── code-reuse-strategy.md # How to reuse Glossary APP code
│   ├── adr/                       # Architecture Decision Records
│   │   ├── template.md            # ADR template
│   │   └── 0001-reference-not-copy-code.md
│   └── getting-started/           # Setup & troubleshooting
│       └── SETUP.md               # Detailed setup guide
│
├── src/                           # 💻 Source code
│   ├── backend/                   # Python FastAPI backend
│   │   ├── core/                  # Config, constants, database
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── api/                   # FastAPI routes
│   │   ├── services/              # Business logic
│   │   │   └── extraction/        # PDF & term extraction
│   │   └── app.py                 # Main application
│   │
│   └── frontend/                  # React frontend
│       ├── public/                # Static assets
│       └── src/
│           ├── components/        # React components
│           ├── pages/             # Page components
│           └── App.tsx            # Main app
│
├── tests/                         # 🧪 Test suite
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
│
├── scripts/                       # 🔨 Utility scripts
│   └── dev-setup.sh               # Development setup automation
│
└── data/                          # 📁 Data storage (gitignored)
    ├── uploads/                   # Uploaded PDFs
    ├── database/                  # SQLite database
    └── cache/                     # Cached data
```

---

## Documentation

### For Developers

- **[CLAUDE.md](CLAUDE.md)** - AI agent guidelines (Design/Coding/Review roles)
- **[Code Reuse Strategy](docs/reference/code-reuse-strategy.md)** - How to reuse Glossary APP components
- **[Architecture Decision Records](docs/adr/)** - Important design decisions
- **[Setup Guide](docs/getting-started/SETUP.md)** - Detailed installation instructions

### For Users

- **[Requirements Document](docs/REQUIREMENTS.md)** - Complete feature requirements and MVP scope
- **[API Documentation](http://localhost:9123/docs)** - Interactive API docs (when server running)

---

## Key Features (MVP)

### ✅ Authoritative Source Integration

- **IATE** (EU Terminology) - API integration
- **NAMUR** (Process Automation) - PDF upload & extraction
- **IEC Electropedia** - Database import (22,798 terms)
- **Manual Entry** - Web interface for custom terms

### ✅ Multi-Language Support

- **German & English** (MVP) - Primary language pair
- **Future**: Spanish, Czech, Chinese, Korean, Japanese, Hindi

### ✅ Language-Internal Thesaurus

- Map synonyms within same language
- Example: "Drucksensor" ↔ "Druckmessumformer" ↔ "Druckaufnehmer"
- Show how different standards use different terms

### ✅ Search & Browse

- Multiple search modes (simple, phrase, boolean, wildcard)
- Browse by source (IATE, NAMUR, IEC)
- Browse by language
- Filter results with source metadata

---

## Technology Stack

### Backend
- **Python 3.12+** - Core language
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database (MVP)
- **Alembic** - Migrations
- **spaCy** - NLP (term extraction)

### Frontend
- **React 18+** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Material-UI (MUI)** - Component library

### Development
- **Git Submodules** - Code reference from Glossary APP
- **pytest** - Backend testing
- **Jest + React Testing Library** - Frontend testing

---

## Code Reuse from Glossary APP

ETEx **references proven components** from the Glossary APP project (located at `vendor/glossary-app/`) using a three-tier strategy:

### Tier 1: Import Directly (Preferred)
```python
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor
```
**Components**: PDF extraction, DeepL client, theme context

### Tier 2: Copy with Attribution (When modifications needed)
```python
"""
Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/services/term_extractor.py
Modifications: [list changes]
"""
```
**Components**: Term extraction utilities, UI components adapted for multi-source

### Tier 3: Reference Only (Inspiration)
Study patterns, document learnings, implement from scratch

**See**: [Code Reuse Strategy Guide](docs/reference/code-reuse-strategy.md)

---

## Development Workflow

### For Single Developer (Primary Use Case)

**Design Phase**:
```bash
# Create spec in .agent/workspace/
# Research vendor/ for reusable patterns
# Finalize spec in docs/architecture/
git commit -m "docs: Add feature spec"
```

**Coding Phase**:
```bash
# Check vendor/ for reusable code
# Implement feature
# Write tests (80%+ coverage)
git commit -m "feat: Implement feature X"
```

**Review Phase**:
```bash
# Run tests, check quality
# Security audit
# Either approve or create fix list
git commit -m "review: Feature X approved"
```

### For Multi-Agent Development (3 Parallel Instances)

Each agent works in separate workspace:
- `.agent/workspace/design/` - Design agent
- `.agent/workspace/coding/` - Coding agent
- `.agent/workspace/review/` - Review agent

**See**: [CLAUDE.md](CLAUDE.md) for complete workflow

---

## Progress Tracking

### Using Git + GitHub Issues (Recommended)

**Status via git**:
```bash
git log --oneline --since="1 week ago"
```

**Status via GitHub**:
- Issues: https://github.com/your-org/etex/issues
- Project Board: https://github.com/your-org/etex/projects

**No manual status files** - they go stale. Use tools that enforce updates automatically.

---

## Testing

### Run Tests

**Backend**:
```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov --cov-report=html

# Specific test
pytest tests/unit/backend/test_pdf_extractor.py
```

**Frontend**:
```bash
cd src/frontend
npm test
```

### Test Requirements

- **Unit tests**: 80%+ coverage
- **Integration tests**: All API endpoints
- **E2E tests**: Critical user flows

---

## Contributing

### Adding New Features

1. **Design**: Create spec in `docs/architecture/`
2. **Code**: Implement with tests
3. **Review**: Self-review before commit
4. **Document**: Update relevant docs
5. **Commit**: Descriptive message with context

### Code Standards

- **Python**: Follow PEP 8, use `black` formatter
- **TypeScript**: Follow Airbnb style guide
- **Tests**: 80%+ coverage required
- **Attribution**: Always credit copied code (Tier 2)

---

## Deployment

### MVP Deployment

**Target**: Development server initially

**Production deployment** if POC successful (Phase 2)

### Environment Variables

**Required**:
- `DATABASE_URL` - Database connection string
- `DEEPL_API_KEY` - DeepL API key (Phase 2)
- `IATE_API_KEY` - IATE API credentials (if required)

**See**: `.env.example` for complete list

---

## Roadmap

### Phase 1: MVP (6 weeks) - IN PROGRESS

- [x] Week 1: Project setup & database
- [ ] Week 2: Document upload & PDF processing
- [ ] Week 3: Term extraction & storage
- [ ] Week 4: IATE API integration
- [ ] Week 5: IEC database import & search
- [ ] Week 6: Manual entry, browse & polish

### Phase 2: Advanced Features (Post-MVP)

- [ ] Internal document processing
- [ ] Deviation checking
- [ ] DeepL integration (Tier 2 translations)
- [ ] Additional languages (Spanish, Czech, Chinese)
- [ ] Synonym auto-detection
- [ ] User accounts & permissions

---

## Support

### Documentation

- **Agent Guidelines**: [CLAUDE.md](CLAUDE.md)
- **Code Reuse**: [docs/reference/code-reuse-strategy.md](docs/reference/code-reuse-strategy.md)
- **ADRs**: [docs/adr/](docs/adr/)

### Troubleshooting

- **Setup issues**: See [docs/getting-started/SETUP.md](docs/getting-started/SETUP.md)
- **API errors**: Check http://localhost:9123/docs for endpoint docs
- **Database issues**: Check `data/database/` permissions

### Getting Help

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check `docs/` folder first
- **Glossary APP Reference**: Study `vendor/glossary-app/` for patterns

---

## License

[Your License Here]

---

## Acknowledgments

- **Glossary APP Project** - Proven components referenced via vendor/
- **IATE** - EU terminology database
- **NAMUR** - Process automation standards
- **IEC Electropedia** - International electrotechnical vocabulary

---

**Built with ❤️ for consistent engineering terminology across languages and standards**

**Last Updated**: 2025-10-31
