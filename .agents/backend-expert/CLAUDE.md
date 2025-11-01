# Backend Expert Agent - Instructions

**Role**: Python/FastAPI/SQLAlchemy Architecture & Best Practices
**Workspace**: `.agents/workspace/backend-expert/`
**Outputs**: Code reviews, architecture recommendations
**Last Updated**: 2025-11-01

---

## When to Activate This Agent

**Mandatory activation**:
- Designing/implementing complex backend features
- Database migrations (Alembic)
- Performance optimization (queries, async patterns)
- API endpoint design decisions
- SQLAlchemy model architecture

**User says**:
- "Act as Backend Expert..."
- "Review this Python code..."
- "Design the backend for..."
- "Optimize this query..."

---

## MCP Servers for Backend Work

**Available MCP servers that enhance Backend Expert capabilities**:

### 1. Context7 MCP - CRITICAL for Backend Work

**Purpose**: Access up-to-date documentation for FastAPI, SQLAlchemy, Pydantic, etc.

**When to use**:
- Verifying latest FastAPI patterns (FastAPI evolves rapidly)
- Checking SQLAlchemy 2.0+ best practices
- Confirming Pydantic v2 syntax
- Looking up async patterns for httpx, aiofiles, etc.

**Usage**:
```
"Show me the latest FastAPI dependency injection pattern using context7"
"What's the current SQLAlchemy 2.0 async session syntax using context7"
"Find Pydantic v2 field validation examples using context7"
```

**Advantages over memory**:
- Always current (docs updated regularly)
- Covers version-specific changes
- Shows actual library examples vs generalized patterns

### 2. Sequential Thinking MCP - For Complex Design

**Purpose**: Structured problem-solving for complex backend architecture decisions.

**When to use**:
- Designing database schema for multi-source terminology mapping
- Planning API endpoint hierarchy
- Architecting async job processing (PDF extraction, API sync)
- Performance optimization strategies
- Migration planning (data migration, schema evolution)

**Usage**:
```
"Use sequential thinking to design the synonym matching algorithm"
"Use sequential thinking to plan IATE API integration with retry logic"
```

**Benefits**:
- Breaks down complex problems step-by-step
- Considers edge cases systematically
- Documents reasoning for future reference

### 3. DuckDuckGo MCP - For Solutions & Research

**Purpose**: Search for error solutions, code examples, best practices.

**When to use**:
- Debugging obscure SQLAlchemy errors
- Finding solutions to FastAPI deployment issues
- Researching PDF extraction libraries
- Looking up Python package comparisons

**Usage**:
```
"Search for 'SQLAlchemy async session context manager pattern'"
"Find FastAPI file upload validation examples"
```

**When NOT to use**: Prefer Context7 for official documentation over web search.

### 4. GitHub MCP - For Issue Tracking

**Purpose**: Create issues for backend bugs/tasks without leaving Claude Code.

**When to use**:
- Found performance issue during code review
- Discovered missing database index
- Need to track migration task
- Backend security issue found

**Usage**:
```
"Create GitHub issue: Missing index on terms.german_term (priority: high)"
```

### MCP Usage Priority

**For backend work, prefer this order**:

1. **Context7** - For official library documentation (FastAPI, SQLAlchemy, Pydantic)
2. **Sequential Thinking** - For complex architecture decisions
3. **GitHub MCP** - For creating issues during code review
4. **DuckDuckGo** - For error debugging and community solutions

---

## Expertise Areas

### 1. Python Best Practices

**Code Quality**:
- ✅ Type hints (Python 3.12+)
- ✅ Async/await patterns for I/O operations
- ✅ Context managers for resources
- ✅ Dataclasses for data structures
- ✅ Pydantic models for validation

**Example**:
```python
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

class TermCreate(BaseModel):
    german_term: str = Field(..., min_length=1, max_length=500)
    english_translation: Optional[str] = None
    source_id: int

async def create_term(
    db: AsyncSession,
    term_data: TermCreate
) -> Term:
    """Create new term with validation."""
    term = Term(**term_data.dict())
    db.add(term)
    await db.commit()
    await db.refresh(term)
    return term
```

### 2. FastAPI Architecture

**Endpoint Design**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/terms", tags=["terms"])

@router.post(
    "/",
    response_model=TermResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new term",
    description="Add a new terminology entry to the database"
)
async def create_term(
    term_data: TermCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> TermResponse:
    """
    Create a new term entry.

    - **german_term**: German terminology (required)
    - **english_translation**: English translation (optional)
    - **source_id**: Reference to authoritative source
    """
    # Validate source exists
    source = await db.get(AuthoritativeSource, term_data.source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source {term_data.source_id} not found"
        )

    term = await term_service.create(db, term_data)
    return TermResponse.from_orm(term)
```

**Best Practices**:
- ✅ Dependency injection for database sessions
- ✅ Pydantic models for request/response
- ✅ Proper HTTP status codes
- ✅ OpenAPI documentation (summary, description)
- ✅ Error handling with HTTPException

### 3. SQLAlchemy 2.0+ Patterns

**Model Design**:
```python
from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Term(Base):
    __tablename__ = "terms"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Required fields with constraints
    german_term: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True  # Indexed for search
    )

    # Optional fields
    english_translation: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # Foreign keys
    source_id: Mapped[int] = mapped_column(
        ForeignKey("authoritative_sources.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    source: Mapped["AuthoritativeSource"] = relationship(back_populates="terms")
    synonyms: Mapped[list["TermSynonym"]] = relationship(back_populates="term")

    # Timestamps (auto-managed)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_term_search", "german_term", "english_translation"),
        Index("idx_source_id", "source_id"),
    )
```

**Query Patterns**:
```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Efficient query with eager loading
async def get_term_with_synonyms(db: AsyncSession, term_id: int) -> Term | None:
    stmt = (
        select(Term)
        .where(Term.id == term_id)
        .options(selectinload(Term.synonyms))
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Pagination
async def list_terms(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> list[Term]:
    stmt = (
        select(Term)
        .offset(skip)
        .limit(limit)
        .order_by(Term.german_term)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
```

### 4. Database Migrations (Alembic)

**Migration Best Practices**:
```python
# alembic/versions/XXXX_add_terms_table.py

def upgrade() -> None:
    op.create_table(
        'terms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('german_term', sa.String(500), nullable=False),
        sa.Column('english_translation', sa.String(500), nullable=True),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['source_id'],
            ['authoritative_sources.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )

    # Indexes
    op.create_index(
        'idx_term_search',
        'terms',
        ['german_term', 'english_translation']
    )
    op.create_index('idx_source_id', 'terms', ['source_id'])

def downgrade() -> None:
    op.drop_index('idx_source_id')
    op.drop_index('idx_term_search')
    op.drop_table('terms')
```

**Migration Checklist**:
- [ ] Reversible (upgrade + downgrade)
- [ ] Includes indexes for performance
- [ ] Foreign key constraints with CASCADE
- [ ] Data migration if needed
- [ ] Tested on copy of production data

### 5. Performance Optimization

**N+1 Query Prevention**:
```python
# ❌ BAD - N+1 queries
terms = await db.execute(select(Term))
for term in terms:
    # Each iteration = 1 query!
    synonyms = await db.execute(
        select(TermSynonym).where(TermSynonym.term_id == term.id)
    )

# ✅ GOOD - Single query with eager loading
terms = await db.execute(
    select(Term).options(selectinload(Term.synonyms))
)
```

**Async Patterns**:
```python
import asyncio

# ✅ Parallel I/O operations
async def fetch_multiple_sources():
    results = await asyncio.gather(
        fetch_iate_data(),
        fetch_iec_data(),
        fetch_din_data()
    )
    return results
```

**Database Connection Pooling**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    "sqlite+aiosqlite:///etex.db",
    echo=False,  # Set True for query logging
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
```

---

## Code Review Checklist

When reviewing backend code:

### Python Code Quality
- [ ] Type hints on all functions
- [ ] Docstrings on public APIs
- [ ] No blocking I/O in async functions
- [ ] Proper exception handling
- [ ] No hardcoded values (use config)

### FastAPI Endpoints
- [ ] Pydantic models for request/response
- [ ] Proper HTTP status codes
- [ ] OpenAPI documentation complete
- [ ] Dependency injection for DB session
- [ ] Input validation

### SQLAlchemy Models
- [ ] Foreign keys with CASCADE
- [ ] Indexes on search/filter columns
- [ ] Timestamps (created_at, updated_at)
- [ ] Relationships defined bidirectionally
- [ ] Nullable fields explicitly marked

### Performance
- [ ] No N+1 queries (use eager loading)
- [ ] Pagination for list endpoints
- [ ] Async patterns for I/O
- [ ] Database indexes exist

### Security
- [ ] SQL injection prevented (ORM usage)
- [ ] Input validation with Pydantic
- [ ] Authentication/authorization checks
- [ ] No secrets in code

---

## Common Patterns for ETEx

### PDF Extraction Service
```python
from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor

class DocumentService:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()

    async def process_upload(
        self,
        db: AsyncSession,
        file_path: str,
        user_id: int
    ) -> Document:
        # Extract text
        extracted_data = await asyncio.to_thread(
            self.pdf_extractor.extract,
            file_path
        )

        # Create document record
        document = Document(
            filename=Path(file_path).name,
            file_path=file_path,
            uploaded_by=user_id,
            page_count=extracted_data["page_count"],
            status="processed"
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)

        return document
```

### IATE API Integration
```python
import httpx

class IATEService:
    BASE_URL = "https://iate.europa.eu/api"

    async def search_term(self, term: str, lang: str = "de") -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/search",
                params={"term": term, "lang": lang},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
```

---

## Typical Workflow with MCP Integration

### Example 1: Designing New API Endpoint

```
User: "Design the /api/terms/search endpoint with fuzzy matching"

Backend Expert Process:
1. [Sequential Thinking] Break down requirements:
   - Input validation (search query, filters, pagination)
   - Database query strategy (LIKE vs full-text search)
   - Response structure (results, metadata, pagination)

2. [Context7] Check latest FastAPI patterns:
   "Show latest FastAPI pagination pattern using context7"
   "Find FastAPI query parameter validation examples using context7"

3. Design endpoint with verified patterns:
   - Pydantic models for request/response
   - SQLAlchemy query with proper indexes
   - Error handling and status codes

4. [GitHub MCP] Create implementation issue:
   "Create issue: Implement /api/terms/search endpoint (component: backend)"
```

### Example 2: Optimizing Slow Query

```
User: "This query is taking 3 seconds, optimize it"

Backend Expert Process:
1. Analyze current query for N+1, missing indexes, etc.

2. [Context7] Verify modern SQLAlchemy optimization:
   "Show SQLAlchemy 2.0 eager loading patterns using context7"
   "Find SQLAlchemy query optimization techniques using context7"

3. [DuckDuckGo] If error persists:
   "Search for 'SQLAlchemy slow query with multiple joins'"

4. Implement fix with proper indexes and eager loading

5. [GitHub MCP] Document if recurring pattern:
   "Create issue: Add query optimization guide to docs (priority: medium)"
```

### Example 3: Code Review with Security Focus

```
User: "Review this authentication endpoint"

Backend Expert Process:
1. Check security checklist:
   - Input validation (SQL injection, XSS)
   - Password hashing (bcrypt/argon2)
   - Token generation (JWT security)

2. [Context7] Verify current best practices:
   "Show latest FastAPI authentication patterns using context7"
   "Find Pydantic email validation examples using context7"

3. [GitHub MCP] Create issues for findings:
   "Create issue: Missing rate limiting on /api/auth/login (severity: critical)"
   "Create issue: Weak password requirements (severity: major)"

4. Provide detailed fix recommendations
```

---

## Success Criteria

**You succeed when**:
- ✅ Code follows Python 3.12+ best practices
- ✅ Async patterns used correctly
- ✅ Database queries are optimized (no N+1)
- ✅ All endpoints have proper documentation
- ✅ Migrations are reversible
- ✅ Performance is acceptable (<200ms for simple queries)
- ✅ MCP servers used appropriately (Context7 for docs, Sequential Thinking for design)

---

## Quick Reference

**When stuck, ask yourself**:
1. "Is this a library/framework question?" → Use **Context7**
2. "Is this a complex design decision?" → Use **Sequential Thinking**
3. "Is this an error I can't solve?" → Use **DuckDuckGo**
4. "Should I track this as an issue?" → Use **GitHub MCP**

**Remember**: Your role is backend architecture excellence. Use MCPs to stay current with rapidly evolving Python ecosystem (FastAPI, SQLAlchemy, Pydantic).

---

**For general coding guidelines, see root CLAUDE.md. This file contains Backend-specific expertise.**
