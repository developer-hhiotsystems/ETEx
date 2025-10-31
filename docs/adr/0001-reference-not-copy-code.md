# ADR-0001: Reference Glossary APP Code, Don't Copy Wholesale

**Status**: ACCEPTED

**Date**: 2025-10-31

**Deciders**: Development Team, Claude Agent Review

**Technical Story**: Building ETEx using proven components from Glossary APP project

---

## Context

ETEx (Engineering Terminology Explorer) needs many features already implemented in the Glossary APP project:
- PDF text extraction with OCR normalization
- Term extraction using NLP
- Translation API integration (DeepL)
- Bilingual UI components
- Search functionality
- Dark mode theming

**The Question**: Should we copy all this code to ETEx, or reference it?

**Forces at Play**:
- **Time pressure**: Don't want to rewrite proven code
- **Maintenance burden**: Copied code must be maintained separately
- **Code quality**: Glossary APP components are production-tested (100+ test cases)
- **Flexibility**: ETEx has different requirements (multi-source, thesaurus, etc.)
- **Attribution**: Need clear provenance of borrowed code
- **Updates**: Bug fixes in Glossary APP should benefit ETEx

---

## Decision

**We will REFERENCE Glossary APP code using a three-tier strategy**, not copy everything wholesale.

### Three-Tier Approach

**Tier 1: Import Directly** (Preferred)
- Use git submodule at `vendor/glossary-app/`
- Import components as-is when no modifications needed
- Example: `from vendor.glossary_app.src.backend.services.pdf_extractor import PDFExtractor`

**Tier 2: Copy with Attribution** (When modifications needed)
- Copy only what needs ETEx-specific changes
- Add attribution header with date and original path
- Document modifications clearly
- Track in CHANGELOG.md

**Tier 3: Reference Only** (Inspiration)
- Study patterns and architecture
- Document learnings in `docs/reference/`
- Implement from scratch for ETEx

### Implementation

1. Add Glossary APP as git submodule: `git submodule add ../Glossary\ APP vendor/glossary-app`
2. Create reuse guide: `docs/reference/code-reuse-strategy.md`
3. Document which components use which tier
4. Maintain attribution for all Tier 2 copies

---

## Consequences

### Positive Consequences

✅ **Zero duplication for Tier 1 imports**
- PDF extractor: 245 lines, 100+ tests → imported, not copied
- Proven stability maintained

✅ **Bug fixes propagate automatically** (Tier 1)
- Update submodule → get latest fixes
- No manual synchronization needed

✅ **Clear code provenance**
- Attribution headers show origin
- Easy to audit what came from where
- Licensing compliance clear

✅ **Flexibility where needed** (Tier 2/3)
- Can modify components for ETEx requirements
- Not locked into Glossary APP's design choices

✅ **Learning resource**
- vendor/ folder serves as reference implementation
- New developers can study proven patterns

### Negative Consequences

⚠️ **Vendor dependency** (Tier 1)
- If Glossary APP changes APIs, Tier 1 imports may break
- Mitigation: Pin submodule to stable commit, update deliberately

⚠️ **Import path complexity** (Tier 1)
- Python imports: `from vendor.glossary_app.src.backend...` (long paths)
- Mitigation: Create wrapper modules if paths become unwieldy

⚠️ **Git submodule learning curve**
- Team must understand submodule commands
- Mitigation: Document clearly in setup guide

⚠️ **Tier 2 maintenance burden**
- Copied code must be maintained manually
- Mitigation: Only use Tier 2 when modifications truly necessary

### Neutral Consequences

➡️ **vendor/ folder in repository**
- Adds ~50MB (git submodule, not full copy)
- Team must run `git submodule update --init`

➡️ **Three-tier decision for each component**
- Must decide: Tier 1, 2, or 3?
- Documented in code-reuse-strategy.md

---

## Options Considered

### Option 1: Copy All Code Wholesale
**Description**: Copy entire Glossary APP codebase to ETEx

**Pros**:
- Complete independence from Glossary APP
- No submodule complexity
- Full control over all code

**Cons**:
- Massive code duplication (~10,000+ lines)
- Bug fixes don't propagate
- Maintenance nightmare (must sync manually)
- Unclear code provenance

**Reason not chosen**: Maintenance burden too high, violates DRY principle

---

### Option 2: Three-Tier Reference Strategy (CHOSEN)
**Description**: Reference with git submodule, import when possible, copy only when needed

**Pros**:
- Minimal duplication (only Tier 2 components)
- Bug fixes propagate automatically (Tier 1)
- Clear attribution and provenance
- Flexibility where needed

**Cons**:
- Submodule learning curve
- Vendor dependency for Tier 1
- Long import paths

**Reason chosen**: Best balance of code reuse, flexibility, and maintainability

---

### Option 3: Monorepo with Shared Packages
**Description**: Restructure both projects into monorepo with shared packages

**Pros**:
- True code sharing (not copying or submodules)
- Shared dependencies managed centrally
- Can refactor shared code safely

**Cons**:
- Major restructuring required (weeks of work)
- Requires monorepo tooling (nx, turborepo, pnpm workspaces)
- More complex CI/CD
- Both projects must move (disruptive)

**Reason not chosen**: Too much upfront investment, overkill for 2 projects

---

### Option 4: Extract Shared Library
**Description**: Extract reusable components to separate npm/PyPI package

**Pros**:
- Clean package boundaries
- Version management via npm/pip
- Can use in other projects

**Cons**:
- Significant packaging work
- Must publish to registry or use private registry
- Versioning overhead
- Overkill for 2 projects

**Reason not chosen**: Premature abstraction, not enough projects to justify

---

## Related Decisions

- Future: ADR-0002 may address vendor code versioning strategy
- Future: ADR-00XX may address monorepo migration if 3+ related projects emerge

---

## Notes

**Key Components Identified for Reuse** (as of 2025-10-31):

**Tier 1 Candidates** (import directly):
- `pdf_extractor.py` - PDF extraction (245 lines, 100+ tests)
- `deepl_client.py` - Translation API (411 lines)
- `ThemeContext.tsx` - Dark mode (React context)
- `SearchBar.tsx` - Search UI component

**Tier 2 Candidates** (copy with attribution):
- `term_extractor.py` - Copy utilities only (clean_term, strip_leading_articles)
- `BilingualCard.tsx` - Adapt for multi-source display
- `base_models.py` - Reference for schema, write new models

**Tier 3 Candidates** (reference only):
- API route structure patterns
- Test organization
- Database migration strategy

**References**:
- [Code Reuse Strategy Guide](../reference/code-reuse-strategy.md)
- [Glossary APP Project](../../vendor/glossary-app/)
- [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

---

**Last Updated**: 2025-10-31
**Status**: ACCEPTED (active)
