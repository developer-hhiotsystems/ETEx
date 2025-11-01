# ETEx - Development Environment Setup Guide

**Last Updated**: 2025-11-01
**For**: Week 1 Development - Issue #8

---

## Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.12+** installed
- ✅ **Node.js 20+ LTS** installed
- ✅ **Git** installed
- ✅ **PowerShell** (Windows) or **Bash** (Linux/Mac)

---

## Quick Setup (Windows)

### Option 1: Automated Setup Script

```powershell
# Run the setup script
.\setup-dev-env.ps1
```

This script will:
1. Check Python and Node.js installations
2. Create Python virtual environment
3. Install Python dependencies
4. Install spaCy language models (German + English)
5. Create .env file from template
6. Create data directories

### Option 2: Manual Setup

If the automated script doesn't work, follow these steps:

#### 1. Find Python Installation

```powershell
# Find Python location
where.exe python

# OR
Get-Command python | Select-Object -ExpandProperty Source
```

**Common Python locations on Windows**:
- `C:\Python312\python.exe`
- `C:\Users\<YourName>\AppData\Local\Programs\Python\Python312\python.exe`
- `C:\Program Files\Python312\python.exe`

#### 2. Create Virtual Environment

```powershell
# Using full Python path if needed
C:\Path\To\Python\python.exe -m venv venv

# OR if Python is in PATH
python -m venv venv
```

#### 3. Activate Virtual Environment

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat
```

You should see `(venv)` in your terminal prompt.

#### 4. Install Python Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### 5. Install spaCy Language Models

```powershell
# German model
python -m spacy download de_core_news_sm

# English model
python -m spacy download en_core_web_sm
```

#### 6. Configure Environment Variables

```powershell
# Copy template
copy .env.example .env

# Edit .env with your favorite editor
notepad .env
```

**Required changes in .env**:
- Add `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
- Add `GITHUB_TOKEN` (if using GitHub MCP)
- Add other API keys as needed

#### 7. Create Data Directories

```powershell
# Create directories
New-Item -ItemType Directory -Force -Path data\database
New-Item -ItemType Directory -Force -Path data\uploads
New-Item -ItemType Directory -Force -Path data\cache
New-Item -ItemType Directory -Force -Path logs
```

---

## Frontend Setup

### 1. Install Node Dependencies

```powershell
cd src\frontend
npm install
cd ..\..
```

### 2. Configure Frontend (if needed)

The frontend should work with default settings pointing to `http://localhost:8000` for the backend API.

---

## Database Setup

### 1. Initialize Alembic (first time only)

```powershell
cd src\backend

# Initialize Alembic (if not already done)
# alembic init alembic

# Run migrations
alembic upgrade head

cd ..\..
```

---

## Running Development Servers

### Terminal 1: Backend (FastAPI)

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run backend
cd src\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend URLs**:
- API: http://localhost:8000
- Health check: http://localhost:8000/health
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

### Terminal 2: Frontend (Vite + React)

```powershell
cd src\frontend
npm run dev
```

**Frontend URL**:
- App: http://localhost:5173

---

## Verification

### 1. Check Backend is Running

```powershell
# In PowerShell or browser
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "service": "ETEx API",
  "version": "0.1.0"
}
```

### 2. Check Frontend is Running

Open browser: http://localhost:5173

You should see the React app (even if it's just a placeholder).

---

## Troubleshooting

### Python not found

**Error**: `python : Die Benennung "python" wurde nicht als Name...`

**Solution**:
1. Find Python installation location
2. Add Python to PATH, OR
3. Use full path to python.exe

**Add Python to PATH (Windows)**:
1. Search for "Environment Variables" in Start Menu
2. Click "Environment Variables"
3. Under "User variables", select "Path", click "Edit"
4. Click "New", add Python directory (e.g., `C:\Python312`)
5. Click "New", add Scripts directory (e.g., `C:\Python312\Scripts`)
6. Click "OK" on all dialogs
7. **Restart PowerShell/Terminal**

### PowerShell execution policy error

**Error**: `cannot be loaded because running scripts is disabled`

**Solution**:
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip install fails

**Error**: Various pip installation errors

**Solutions**:
```powershell
# Update pip
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -v -r requirements.txt
```

### spaCy model download fails

**Error**: `Can't find model 'de_core_news_sm'`

**Solution**:
```powershell
# Download models directly
python -m spacy download de_core_news_sm --direct

# OR download from GitHub releases and install manually
# See: https://github.com/explosion/spacy-models/releases
```

### Port already in use

**Error**: `Address already in use`

**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace <PID> with actual PID)
taskkill /F /PID <PID>

# OR use different port
uvicorn main:app --port 8001 --reload
```

---

## Next Steps After Setup

Once both servers are running:

1. ✅ Mark Issue #8 as complete
2. ➡️ Move to Issue #5: Initialize FastAPI backend with Alembic
3. ➡️ Move to Issue #4: Create database schema with SQLAlchemy models
4. ➡️ Move to Issue #6: Initialize React frontend with Vite + MUI

---

## Development Workflow

### Daily Development

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Pull latest changes
git pull

# 3. Install any new dependencies
pip install -r requirements.txt
cd src\frontend && npm install && cd ..\..

# 4. Run migrations
cd src\backend && alembic upgrade head && cd ..\..

# 5. Start servers (2 terminals)
# Terminal 1: cd src\backend && uvicorn main:app --reload
# Terminal 2: cd src\frontend && npm run dev
```

### Before Committing

```powershell
# Format code
black src/backend/

# Run linter
ruff check src/backend/

# Run tests
pytest

# Run frontend tests
cd src\frontend && npm test && cd ..\..
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Alembic Docs**: https://alembic.sqlalchemy.org
- **Vite Docs**: https://vitejs.dev
- **React Docs**: https://react.dev
- **MUI Docs**: https://mui.com

---

**Questions?** See [CLAUDE.md](CLAUDE.md) for agent-specific workflows or create a GitHub issue.
