# ETEx Setup Guide

**Last Updated**: 2025-10-31

---

## Prerequisites

- **Python 3.12+** installed
- **Node.js 18+** installed
- **Git** installed (for version control)
- **Windows** (this guide is Windows-specific)

---

## Quick Setup (5 Minutes)

### 1. Navigate to ETEx Project

```bash
cd "C:\Users\developer\Documents\Coding Projects\ETEx"
```

### 2. Setup Vendor Reference to Glossary APP

Since both projects are on the same machine, we'll use a directory junction (Windows symlink):

**Option A: Create Junction (Recommended)**:
```cmd
# Run as Administrator or in elevated command prompt
cd vendor
mklink /J glossary-app "..\..\Glossary APP"
```

**Option B: Manual Reference** (if junction fails):
Just note the path and update imports to use absolute paths:
```python
# Instead of:
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

# Use:
import sys
sys.path.append(r'C:\Users\developer\Documents\Coding Projects\Glossary APP')
from src.backend.services.pdf_extractor import PDFExtractor
```

**Verify vendor/ setup**:
```bash
# Should show Glossary APP files
ls vendor/glossary-app/src/backend/services/
```

### 3. Setup Python Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies (create requirements.txt first - see below)
pip install -r requirements.txt
```

**Create `requirements.txt`** (if it doesn't exist):
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
python-multipart==0.0.6
aiofiles==23.2.1
```

### 4. Setup React Frontend

```bash
cd src/frontend

# Install dependencies
npm install

# Return to root
cd ../..
```

### 5. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your settings
notepad .env
```

**Minimal `.env` for MVP**:
```env
# Database
DATABASE_URL=sqlite:///./data/database/etex.db

# API Keys (Phase 2)
# DEEPL_API_KEY=your-key-here
# IATE_API_KEY=your-key-here

# Development
DEBUG=True
LOG_LEVEL=INFO
```

### 6. Initialize Database

```bash
cd src/backend

# Create database directory
mkdir -p ../../data/database

# Run migrations (once we have them)
# alembic upgrade head

cd ../..
```

### 7. Run Development Servers

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

## Detailed Setup

### Python Environment Setup

#### 1. Install Python Dependencies

```bash
# Activate venv
venv\Scripts\activate

# Core dependencies
pip install fastapi uvicorn[standard] sqlalchemy alembic pydantic

# Database
pip install aiosqlite  # Async SQLite

# File handling
pip install python-multipart aiofiles

# NLP (for term extraction)
pip install spacy
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm

# PDF processing (reuse from Glossary APP)
# Will import from vendor/glossary-app/

# Save dependencies
pip freeze > requirements.txt
```

#### 2. Database Setup

**Create database directories**:
```bash
mkdir data\database
mkdir data\uploads
mkdir data\cache
```

**Initialize Alembic** (database migrations):
```bash
cd src/backend
alembic init alembic
```

Edit `alembic.ini`:
```ini
sqlalchemy.url = sqlite:///../../data/database/etex.db
```

Edit `alembic/env.py`:
```python
# Import your models
from src.backend.models import Base
target_metadata = Base.metadata
```

**Create initial migration**:
```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Frontend Setup

#### 1. Initialize React Project

If `src/frontend` doesn't have package.json:

```bash
cd src/frontend
npm create vite@latest . -- --template react-ts
```

#### 2. Install Dependencies

```bash
# Core dependencies
npm install react react-dom
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled

# Routing
npm install react-router-dom

# HTTP client
npm install axios

# Development dependencies
npm install -D @types/react @types/react-dom
npm install -D vite @vitejs/plugin-react

# Testing
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

#### 3. Configure Vite

**`vite.config.ts`**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
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

### Vendor Code Reference Setup

#### Option 1: Git Submodule (if Glossary APP is git repo)

```bash
cd vendor
git submodule add path/to/glossary-app glossary-app
git submodule update --init
```

#### Option 2: Directory Junction (Windows)

```cmd
# Run as Administrator
cd vendor
mklink /J glossary-app "..\..\Glossary APP"
```

**Verify**:
```bash
ls vendor/glossary-app/src/backend/services/
# Should show: pdf_extractor.py, term_extractor.py, etc.
```

#### Option 3: Python Path (fallback)

If vendor/ setup fails, add to Python path:

**`src/backend/core/config.py`**:
```python
import sys
from pathlib import Path

# Add Glossary APP to Python path
GLOSSARY_APP_PATH = Path(__file__).parent.parent.parent.parent.parent / "Glossary APP"
sys.path.insert(0, str(GLOSSARY_APP_PATH))
```

---

## Troubleshooting

### "Module not found: vendor.glossary_app"

**Cause**: vendor/glossary-app not set up correctly

**Fix**:
1. Verify vendor/glossary-app exists: `ls vendor/glossary-app/`
2. Try creating junction as Administrator
3. Or use absolute import (Option 3 above)

### "Permission denied" when creating junction

**Cause**: Need Administrator rights

**Fix**:
```cmd
# Open Command Prompt as Administrator (Right-click → Run as Administrator)
cd "C:\Users\developer\Documents\Coding Projects\ETEx\vendor"
mklink /J glossary-app "..\..\Glossary APP"
```

### Backend won't start - "No module named 'fastapi'"

**Cause**: Virtual environment not activated or dependencies not installed

**Fix**:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend won't start - "Cannot find module 'react'"

**Cause**: Dependencies not installed

**Fix**:
```bash
cd src/frontend
npm install
```

### Database not found

**Cause**: Database directory doesn't exist

**Fix**:
```bash
mkdir -p data/database
cd src/backend
alembic upgrade head
```

### Port 9123 or 5173 already in use

**Cause**: Another process using the port

**Fix**:
```bash
# Find and kill process on port 9123 (Windows)
netstat -ano | findstr :9123
taskkill /PID <process-id> /F

# Or use different port
uvicorn app:app --host 0.0.0.0 --port 9124
```

---

## Verification Checklist

After setup, verify everything works:

**Backend**:
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] vendor/glossary-app accessible
- [ ] Database exists (`ls data/database/`)
- [ ] Server starts: `uvicorn app:app --host 0.0.0.0 --port 9123`
- [ ] API docs load: http://localhost:9123/docs

**Frontend**:
- [ ] Dependencies installed (`npm list`)
- [ ] Dev server starts: `npm run dev`
- [ ] App loads: http://localhost:5173
- [ ] No console errors

**Integration**:
- [ ] Frontend can call backend API
- [ ] CORS configured correctly
- [ ] File uploads work (once implemented)

---

## Next Steps

Once setup is complete:

1. **Read Documentation**:
   - [CLAUDE.md](../../CLAUDE.md) - Agent guidelines
   - [Code Reuse Strategy](../reference/code-reuse-strategy.md) - How to use Glossary APP code
   - [ADRs](../adr/) - Important decisions

2. **Start Development**:
   - Follow [Week 1 tasks](../REQUIREMENTS.md#implementation-plan-6-week-mvp)
   - Create database models
   - Setup API endpoints
   - Build frontend components

3. **Explore Vendor Code**:
   ```bash
   # Check what's available
   ls vendor/glossary-app/src/backend/services/
   ls vendor/glossary-app/src/frontend/src/components/

   # Read code-reuse-strategy for guidance
   cat docs/reference/code-reuse-strategy.md
   ```

---

## Development Workflow

### Daily Development

**Start servers**:
```bash
# Terminal 1 - Backend
cd src/backend
../../venv/Scripts/activate
../../venv/Scripts/uvicorn app:app --host 0.0.0.0 --port 9123 --reload

# Terminal 2 - Frontend
cd src/frontend
npm run dev
```

**Run tests**:
```bash
# Backend tests
cd src/backend
pytest tests/

# Frontend tests
cd src/frontend
npm test
```

**Make changes**:
1. Edit code
2. Tests auto-run (--reload flag)
3. Check browser/API docs for results
4. Commit when done

### Git Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(module): Brief description

- Detail 1
- Detail 2
- Progress: Week X - Y% complete"

# Push (if remote configured)
git push origin master
```

---

## Getting Help

**Documentation**:
- [README.md](../../README.md) - Project overview
- [REQUIREMENTS.md](../REQUIREMENTS.md) - Complete feature spec
- [Code Reuse Strategy](../reference/code-reuse-strategy.md) - Glossary APP reference guide

**Common Issues**:
- Check this SETUP.md Troubleshooting section
- Search [GitHub Issues](link-to-issues)
- Review Glossary APP for similar implementations

---

**Setup Complete!** 🎉

You're now ready to start building ETEx. Begin with Week 1 tasks from [REQUIREMENTS.md](../REQUIREMENTS.md#implementation-plan-6-week-mvp).

**Last Updated**: 2025-10-31
