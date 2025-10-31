# MCP Server Integration for ETEx

**Purpose**: Enhance Claude Code's capabilities with Model Context Protocol (MCP) servers
**Last Updated**: 2025-11-01
**Status**: Recommended for ETEx project

---

## Overview

MCP servers extend Claude Code's capabilities by providing specialized tools and context. For the ETEx project, we've identified 9 high-value MCP servers that align with our 6-week MVP timeline and technical stack.

---

## Priority 1: Essential for ETEx (Install First)

### 1. GitHub MCP Server ⭐ CRITICAL

**Why Essential for ETEx**:
- Manage 22 labels, 6 milestones, and project board automatically
- Create/close issues without leaving Claude Code
- Review PRs and commit history in context
- Essential for Issue Manager and Project Manager agents

**Installation**:
```bash
# Remote server connection (recommended)
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# You'll be prompted for GitHub PAT (Personal Access Token)
# Create token at: https://github.com/settings/tokens
# Required scopes: repo, workflow, write:packages, read:org
```

**Configuration**:
```json
{
  "mcpServers": {
    "github": {
      "transport": {
        "type": "http",
        "url": "https://api.githubcopilot.com/mcp/"
      },
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_PAT"
      }
    }
  }
}
```

**ETEx Use Cases**:
- Issue Manager: "Create issue for Week 2 PDF upload feature with high priority"
- Project Manager: "Show all blocked issues in Week 3 milestone"
- Review Coordinator: "List all open PRs that modify scripts/"

---

### 2. Sequential Thinking MCP Server ⭐ CRITICAL

**Why Essential for ETEx**:
- Design Agent needs structured problem-solving for feature specs
- Backend/Frontend Experts benefit from step-by-step architecture decisions
- Critical for complex tasks like database schema design, API contracts

**Installation**:
```bash
# Standard installation
claude mcp add sequential-thinking npx -- -y @modelcontextprotocol/server-sequential-thinking

# For Windows:
claude mcp add sequential-thinking cmd -- /c npx -y @modelcontextprotocol/server-sequential-thinking
```

**ETEx Use Cases**:
- Design Agent: "Use sequential thinking to design the term synonym linking architecture"
- Backend Expert: "Think through the N+1 query prevention strategy step by step"
- Project Manager: "Analyze Week 3 blockers and create resolution plan"

**Activation Pattern**:
Add to prompts: "use sequential thinking" or "think through this step by step"

---

### 3. Knowledge Graph Memory MCP Server ⭐ CRITICAL

**Why Essential for ETEx**:
- Retain context about ETEx's 6-week MVP plan across sessions
- Remember vendor/glossary-app code reuse decisions
- Maintain understanding of agent roles and responsibilities
- Prevent repetitive explanations about project structure

**Installation**:
```bash
# Clone the memory server
git clone https://github.com/modelcontextprotocol/server-memory.git
cd server-memory
npm install

# Configure in Claude Code
claude mcp add knowledge-graph node -- /path/to/server-memory/build/index.js
```

**Configuration**:
```json
{
  "mcpServers": {
    "knowledge-graph": {
      "command": "node",
      "args": ["/path/to/server-memory/build/index.js"],
      "env": {
        "MEMORY_PATH": "c:/Users/developer/Documents/Coding Projects/ETEx/.agents/memory/"
      }
    }
  }
}
```

**ETEx Use Cases**:
- Remember: "ETEx uses SQLAlchemy 2.0 with async patterns"
- Recall: "Week 2 milestone includes PDF extraction from vendor/glossary-app"
- Context: "Backend Expert agent mandatory for Python/FastAPI work"

---

## Priority 2: Highly Recommended

### 4. Context7 MCP Server ⭐ HIGH VALUE

**Why Recommended for ETEx**:
- Get latest FastAPI, SQLAlchemy 2.0, React 18 documentation
- Ensure MUI (Material-UI) code examples are current
- Access latest TypeScript patterns and best practices

**Installation**:
```bash
# Remote server connection (recommended)
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# You'll need a Context7 API key from https://context7.com
```

**Configuration**:
```json
{
  "mcpServers": {
    "context7": {
      "transport": {
        "type": "http",
        "url": "https://mcp.context7.com/mcp"
      },
      "headers": {
        "Authorization": "Bearer YOUR_CONTEXT7_API_KEY"
      }
    }
  }
}
```

**ETEx Use Cases**:
- Backend Expert: "Generate SQLAlchemy 2.0 async query pattern - use context7"
- Frontend Expert: "Create MUI DataGrid with latest v5 features - use context7"
- Coding Agent: "Show current FastAPI file upload best practices - use context7"

**Usage Pattern**:
Add "use context7" to any prompt requiring current library documentation.

---

### 5. Playwright MCP Server ⭐ HIGH VALUE

**Why Recommended for ETEx**:
- E2E testing for React frontend (Week 6 polish phase)
- Automate UI testing for search, browse, manual entry features
- Screenshot capture for design reviews

**Installation**:
```bash
# Standard installation
claude mcp add playwright npx -- @playwright/mcp@latest

# For Windows:
claude mcp add playwright cmd -- /c npx @playwright/mcp@latest
```

**ETEx Use Cases**:
- Testing Agent: "Test the term search workflow end-to-end using Playwright"
- Frontend Expert: "Capture screenshots of bilingual term display on mobile/desktop"
- Design Agent: "Verify search UI meets accessibility requirements"

---

### 6. DuckDuckGo MCP Server ⭐ HIGH VALUE

**Why Recommended for ETEx**:
- Search for current Python/FastAPI error solutions
- Find latest IATE API documentation
- Look up IEC Electropedia integration examples
- No API key required (unlike Google Custom Search)

**Installation**:
```bash
# Clone the DuckDuckGo MCP server
git clone https://github.com/modelcontextprotocol/servers.git
cd servers/src/duckduckgo
npm install

# Configure in Claude Code
claude mcp add duckduckgo node -- /path/to/servers/src/duckduckgo/index.js
```

**ETEx Use Cases**:
- Backend Expert: "Search for SQLAlchemy async session best practices 2025"
- Coding Agent: "Find latest spaCy German NLP examples"
- Issue Manager: "Look up how to handle IATE API rate limiting"

---

## Priority 3: Useful but Optional

### 7. Apidog MCP Server

**Why Useful for ETEx**:
- Generate TypeScript types from FastAPI OpenAPI spec
- Create API client code for frontend
- Validate API responses match spec

**Installation**:
```bash
# After FastAPI app is running and generates OpenAPI spec
claude mcp add apidog -- npx -y apidog-mcp-server@latest --oas=http://localhost:8000/openapi.json

# Or use local file after Week 1
claude mcp add apidog -- npx -y apidog-mcp-server@latest --oas=c:/Users/developer/Documents/Coding\ Projects/ETEx/docs/api/openapi.json
```

**ETEx Use Cases** (Week 2+):
- Frontend Expert: "Generate TypeScript types for all /api/terms endpoints"
- Design Agent: "Validate API spec follows REST conventions"
- Testing Agent: "Generate mock API responses for testing"

---

### 8. Memory Bank MCP Server

**Why Useful for ETEx**:
- Alternative to Knowledge Graph Memory (simpler, file-based)
- Good for storing code snippets from vendor/glossary-app
- Hierarchical organization of project knowledge

**Installation**:
```bash
# Clone the memory bank server
git clone https://github.com/modelcontextprotocol/server-memory.git
cd server-memory
npm install

# Configure
claude mcp add memory-bank node -- /path/to/server-memory/index.js
```

**ETEx Use Cases**:
- "Remember this SQLAlchemy pattern for term synonym queries"
- "Store this MUI theme configuration for ETEx"
- "Recall the code reuse attribution template"

---

### 9. MCP Compass

**Why Useful**:
- Discover new MCP servers as ecosystem grows
- Find specialized tools for specific ETEx needs
- Natural language MCP server search

**Installation**:
```bash
# Install MCP Compass
npm install -g @mcptools/compass

# Configure
claude mcp add compass npx -- @mcptools/compass
```

**ETEx Use Cases**:
- "Find MCP servers for PDF processing"
- "Are there any MCP servers for database migrations?"
- "Discover MCP servers for internationalization"

---

## Installation Priority Order

**Week 0 (Before Development Starts)**:
1. ✅ GitHub MCP - Essential for issue/PR management
2. ✅ Sequential Thinking MCP - Critical for design/architecture
3. ✅ Knowledge Graph Memory MCP - Retain ETEx context

**Week 1-2 (Backend Setup)**:
4. Context7 MCP - Latest FastAPI/SQLAlchemy docs
5. DuckDuckGo MCP - Error solutions and examples

**Week 3-4 (API Development)**:
6. Apidog MCP - API spec validation and client generation

**Week 5-6 (Frontend & Testing)**:
7. Playwright MCP - E2E testing automation

**Optional (As Needed)**:
8. Memory Bank MCP - If Knowledge Graph insufficient
9. MCP Compass - To discover specialized tools

---

## Configuration File Template

Create `.claude/settings.json` (or `.claude/settings.local.json`):

```json
{
  "mcpServers": {
    "github": {
      "transport": {
        "type": "http",
        "url": "https://api.githubcopilot.com/mcp/"
      },
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_PAT"
      }
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "knowledge-graph": {
      "command": "node",
      "args": ["c:/path/to/server-memory/build/index.js"],
      "env": {
        "MEMORY_PATH": "c:/Users/developer/Documents/Coding Projects/ETEx/.agents/memory/"
      }
    },
    "context7": {
      "transport": {
        "type": "http",
        "url": "https://mcp.context7.com/mcp"
      },
      "headers": {
        "Authorization": "Bearer YOUR_CONTEXT7_API_KEY"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "duckduckgo": {
      "command": "node",
      "args": ["c:/path/to/servers/src/duckduckgo/index.js"]
    }
  }
}
```

---

## Agent-Specific MCP Usage

### Issue Manager Agent
**Primary MCPs**: GitHub
```
Example: "Create Week 2 issue for PDF upload with labels type:feature,priority:high"
```

### Design Agent
**Primary MCPs**: Sequential Thinking, Context7
```
Example: "Use sequential thinking to design database schema, reference latest SQLAlchemy 2.0 docs with context7"
```

### Backend Expert Agent
**Primary MCPs**: Context7, DuckDuckGo, Sequential Thinking
```
Example: "Show latest FastAPI async patterns using context7, search for N+1 query solutions"
```

### Frontend Expert Agent
**Primary MCPs**: Context7, Playwright
```
Example: "Generate React 18 component with latest MUI patterns using context7"
```

### Project Manager Agent
**Primary MCPs**: GitHub, Sequential Thinking
```
Example: "Analyze Week 3 velocity using GitHub data, use sequential thinking for sprint planning"
```

### Coding Agent
**Primary MCPs**: Context7, Apidog, DuckDuckGo
```
Example: "Implement API endpoint using context7 for latest FastAPI patterns"
```

### Testing Agent
**Primary MCPs**: Playwright, Apidog
```
Example: "Run E2E tests for search UI using Playwright"
```

### Review Coordinator
**Primary MCPs**: GitHub, Sequential Thinking
```
Example: "Review CLAUDE.md changes in PR #5 using GitHub MCP"
```

---

## Verification Commands

**After installation, verify each MCP**:
```bash
# List all installed MCPs
claude mcp list

# Test GitHub MCP
claude mcp test github "List open issues"

# Test Sequential Thinking
claude mcp test sequential-thinking "Break down: Design database schema"

# Test Context7
claude mcp test context7 "Get latest FastAPI documentation"
```

---

## Troubleshooting

### GitHub MCP Not Working
```bash
# Check token scopes
gh auth status

# Regenerate token with correct scopes
# repo, workflow, write:packages, read:org
```

### Sequential Thinking Not Activating
- Ensure you include "use sequential thinking" in prompt
- Verify installation: `claude mcp list`

### Context7 Rate Limits
- Free tier: 100 requests/day
- Upgrade to paid plan for production use
- Cache responses when possible

### Knowledge Graph Memory Storage Full
```bash
# Check memory size
ls -lh .agents/memory/

# Clean old memories if needed
# (Be careful - this is destructive)
rm -rf .agents/memory/old/*
```

---

## Security Considerations

**API Keys and Tokens**:
- ✅ Store in `.claude/settings.local.json` (gitignored)
- ❌ Never commit API keys to repository
- ✅ Use environment variables for CI/CD
- ✅ Rotate GitHub PATs every 90 days

**File Access**:
- Knowledge Graph Memory: Limited to `.agents/memory/` directory
- File System MCP: NOT RECOMMENDED (too broad access)

**Network Access**:
- GitHub MCP: github.com only
- Context7 MCP: context7.com only
- DuckDuckGo MCP: duckduckgo.com only

---

## Cost Analysis

| MCP Server | Cost | Notes |
|------------|------|-------|
| GitHub | Free | Requires GitHub account |
| Sequential Thinking | Free | Open source |
| Knowledge Graph Memory | Free | Local storage |
| Context7 | Free tier: 100/day | Paid plans available |
| Playwright | Free | Open source |
| DuckDuckGo | Free | No API key required |
| Apidog | Free | Open source |
| Memory Bank | Free | Local storage |
| MCP Compass | Free | Open source |

**Total Cost for ETEx**: $0 (using free tiers)

---

## Success Metrics

**MCP integration succeeds when**:
- ✅ Issue Manager creates GitHub issues without manual intervention
- ✅ Design Agent produces better architecture using sequential thinking
- ✅ Context is retained across sessions (Knowledge Graph Memory)
- ✅ Code examples match latest library versions (Context7)
- ✅ E2E tests run automatically (Playwright)
- ✅ Developer velocity increases by 20%+ (less context switching)

---

## Next Steps

1. **Week 0 Setup** (Before starting Week 1):
   - Install GitHub, Sequential Thinking, Knowledge Graph Memory MCPs
   - Configure `.claude/settings.local.json`
   - Verify all 3 MCPs working: `claude mcp list`

2. **Week 1 Enhancement**:
   - Add Context7 and DuckDuckGo MCPs
   - Test with Backend Expert agent

3. **Week 3 API Phase**:
   - Add Apidog MCP after OpenAPI spec generated
   - Generate TypeScript API client

4. **Week 5 Testing Phase**:
   - Add Playwright MCP
   - Create E2E test suite

---

**For installation help, see**: [Claude Code MCP Documentation](https://docs.claude.com/en/docs/claude-code/mcp)
**For MCP ecosystem updates, use**: MCP Compass to discover new servers

---

**Last Updated**: 2025-11-01
**Maintained By**: Project Manager Agent
**Review Schedule**: Weekly during sprint planning
