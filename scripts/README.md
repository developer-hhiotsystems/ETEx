# ETEx Scripts

**Purpose**: Organized collection of application and development scripts
**Last Updated**: 2025-10-31

---

## Directory Structure

```
scripts/
├── app/          # Application scripts (runtime, production)
├── dev/          # Development helper scripts
│   ├── setup/    # Initial setup & environment
│   ├── github/   # GitHub workflow automation
│   ├── testing/  # Test execution & coverage
│   └── quality/  # Code quality & linting
├── docs/         # Documentation generation
└── data/         # Data management & backups
```

---

## Quick Links

- **[Application Scripts](app/README.md)** - Start servers, run migrations, seed data
- **[Development Scripts](dev/README.md)** - Setup, GitHub, testing, quality
- **[Documentation Scripts](docs/README.md)** - Generate docs, export to Wiki
- **[Data Scripts](data/README.md)** - Backup, restore, import data

---

## Script Organization Philosophy

### Application Scripts (`app/`)
Scripts that **end users or operators** run in production/staging environments.
- Start/stop services
- Run database migrations
- Deploy application

### Development Scripts (`dev/`)
Scripts that **developers** use during development workflow.
- Setup environment
- Create GitHub issues
- Run tests
- Check code quality

### Documentation Scripts (`docs/`)
Scripts for **generating or exporting** documentation.
- API reference generation
- Wiki exports
- Changelog creation

### Data Scripts (`data/`)
Scripts for **data operations**.
- Database backups
- Import external data
- Export reports

---

## Naming Conventions

**Format**: `<verb>-<noun>.ps1`

**Examples**:
- `start-backend.ps1`
- `create-labels.ps1`
- `run-tests.ps1`
- `backup-database.ps1`

See [Scripts Organization Guide](../docs/reference/scripts-organization.md) for complete conventions.

---

## Getting Started

### For First-Time Setup
```powershell
# 1. Install dependencies
.\dev\setup\install-dependencies.ps1

# 2. Setup environment
.\dev\setup\setup-environment.ps1

# 3. Initialize database
.\app\migrate-database.ps1
```

### For Daily Development
```powershell
# Start backend
.\app\start-backend.ps1

# Start frontend (in another terminal)
.\app\start-frontend.ps1

# Run tests
.\dev\testing\run-all-tests.ps1
```

### For GitHub Workflow
```powershell
# Create labels
.\dev\github\create-agent-labels.ps1

# Create Week 1 issues
.\dev\github\create-week1-issues.ps1
```

---

## Documentation

- **Organization Guide**: [docs/reference/scripts-organization.md](../docs/reference/scripts-organization.md)
- **Development Guidelines**: See individual category READMEs
- **Troubleshooting**: See category-specific READMEs

---

## Contributing Scripts

When adding new scripts:

1. **Choose correct category** (app/dev/docs/data)
2. **Follow naming conventions** (verb-noun.ps1)
3. **Add script header** (synopsis, description, examples)
4. **Add to category README** (update script list)
5. **Test script** (include dry-run mode if applicable)

See [Scripts Organization Guide](../docs/reference/scripts-organization.md) for complete guidelines.

---

**For detailed information, see**: [Scripts Organization Guide](../docs/reference/scripts-organization.md)
