# MCP Server Installation Guide - ETEx Project

**Date**: 2025-11-01
**Based on**: Agent consultation feedback (all 8 agents consulted)
**Installation Time**: ~20 minutes for all 5 MCPs

---

## Agent Consensus Results

After consulting all 8 agents, here are the approved MCPs:

| MCP Server | Priority | Agents Supporting | When to Install |
|------------|----------|-------------------|-----------------|
| GitHub MCP | CRITICAL | 8/8 | Week 0 (Now) |
| Sequential Thinking MCP | CRITICAL | 8/8 | Week 0 (Now) |
| Context7 MCP | HIGH | 6/8 | Week 0 (Now) |
| Playwright MCP | HIGH (Specialized) | 5/8 | Week 5-6 |
| DuckDuckGo MCP | MEDIUM | 3/8 | Week 1-2 (Optional) |

**Total Cost**: $0 (all free tiers)

---

## Installation Steps

### Prerequisites

Before installing MCPs, ensure you have:
- ✅ Claude Code installed and running
- ✅ Node.js 18+ installed (for some MCPs)
- ✅ Git installed
- ✅ GitHub account with Personal Access Token ready

---

## Step 1: GitHub MCP (CRITICAL - 8/8 Agents)

### Why Install This?
- **Issue Manager**: 80% faster issue creation/closure
- **Project Manager**: Automated sprint velocity tracking
- **All Agents**: Eliminate context switching to GitHub UI

### Installation

**Option A: Via Claude Code UI (Recommended)**
1. Open Claude Code settings
2. Navigate to MCP Servers section
3. Click "Add MCP Server"
4. Select "HTTP Transport"
5. Enter:
   - Name: `github`
   - URL: `https://api.githubcopilot.com/mcp/`
   - Authorization header: `Bearer YOUR_GITHUB_PAT`

**Option B: Via Configuration File**
1. Create/edit `.claude/settings.local.json`
2. Add GitHub MCP configuration (see below)

### Get GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages to GitHub Package Registry)
   - ✅ `read:org` (Read org and team membership)
4. Generate token
5. Copy token immediately (you won't see it again)

### Configuration (`.claude/settings.local.json`)

```json
{
  "mcpServers": {
    "github": {
      "transport": {
        "type": "http",
        "url": "https://api.githubcopilot.com/mcp/"
      },
      "headers": {
        "Authorization": "Bearer ghp_YourGitHubTokenHere"
      }
    }
  }
}
```

### Verify Installation

Ask Claude Code:
```
"List all open issues in the ETEx repository using GitHub MCP"
```

Expected: Should return current open issues without errors.

---

## Step 2: Sequential Thinking MCP (CRITICAL - 8/8 Agents)

### Why Install This?
- **Design Agent**: Structured spec creation (30% quality improvement)
- **All Experts**: Better architecture decisions
- **Project Manager**: Risk assessment and sprint planning

### Installation

**Windows**:
```bash
# Via command (if claude CLI available)
claude mcp add sequential-thinking cmd -- /c npx -y @modelcontextprotocol/server-sequential-thinking
```

**macOS/Linux**:
```bash
claude mcp add sequential-thinking npx -- -y @modelcontextprotocol/server-sequential-thinking
```

**Via Configuration File** (if CLI not available):

Add to `.claude/settings.local.json`:
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

### Verify Installation

Ask Claude Code:
```
"Use sequential thinking to analyze: Should we use SQLite or PostgreSQL for ETEx MVP?"
```

Expected: Should see step-by-step analysis with structured reasoning.

---

## Step 3: Context7 MCP (HIGH - 6/8 Agents)

### Why Install This?
- **Backend Expert**: Latest FastAPI/SQLAlchemy/Pydantic docs (30% faster dev)
- **Frontend Expert**: Latest React 18/MUI v5/TypeScript docs (35% faster dev)
- **Design Agent**: Research current best practices

### Installation

**Get Context7 API Key**:
1. Go to https://context7.com
2. Sign up (free tier: 100 requests/day)
3. Navigate to API Keys section
4. Generate new API key
5. Copy key

**Add to `.claude/settings.local.json`**:
```json
{
  "mcpServers": {
    "context7": {
      "transport": {
        "type": "http",
        "url": "https://mcp.context7.com/mcp"
      },
      "headers": {
        "Authorization": "Bearer your_context7_api_key_here"
      }
    }
  }
}
```

### Verify Installation

Ask Claude Code:
```
"Show me the latest FastAPI async file upload patterns using context7"
```

Expected: Should return current FastAPI documentation snippets.

### Free Tier Limits
- 100 requests/day
- Sufficient for 6-week MVP
- Consider paid plan ($19/month) post-MVP if needed

---

## Step 4: Playwright MCP (HIGH - 5/8 Agents, Install Week 5-6)

### Why Install This?
- **Testing Agent**: E2E testing (Week 6 MVP polish)
- **Frontend Expert**: Component testing, accessibility audits
- **Review Coordinator**: UI verification

### When to Install
- **Not needed until Week 5-6** (frontend testing phase)
- Can skip for now if focusing on backend (Week 1-2)

### Installation (When Ready)

**Windows**:
```bash
claude mcp add playwright cmd -- /c npx @playwright/mcp@latest
```

**macOS/Linux**:
```bash
claude mcp add playwright npx -- @playwright/mcp@latest
```

**Via Configuration File**:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### Verify Installation (Week 5-6)

Ask Claude Code:
```
"Use Playwright to test the term search workflow: navigate to search page, enter 'Drucksensor', verify results"
```

Expected: Should launch browser and execute test.

---

## Step 5: DuckDuckGo MCP (OPTIONAL - 3/8 Agents)

### Why Install This? (Optional)
- **Backend Expert**: Error research, async edge cases
- **Testing Agent**: Test failure diagnosis
- **Frontend Expert**: React error solutions

### Why Optional?
- Context7 already covers most documentation needs
- Web search can be done manually if needed
- Not critical for MVP

### Installation (If Desired)

**Step 1: Clone MCP Servers Repository**
```bash
git clone https://github.com/modelcontextprotocol/servers.git
cd servers/src/duckduckgo
npm install
```

**Step 2: Add to Configuration**

Add to `.claude/settings.local.json`:
```json
{
  "mcpServers": {
    "duckduckgo": {
      "command": "node",
      "args": ["c:/path/to/servers/src/duckduckgo/index.js"]
    }
  }
}
```

Replace `c:/path/to/servers` with actual path where you cloned the repo.

### Verify Installation

Ask Claude Code:
```
"Search for 'SQLAlchemy async session scope best practices 2025' using DuckDuckGo"
```

Expected: Should return recent search results.

---

## Complete Configuration Example

Here's a complete `.claude/settings.local.json` with all 5 MCPs:

```json
{
  "$schema": "https://raw.githubusercontent.com/anthropics/claude-code/main/schema/settings.schema.json",
  "mcpServers": {
    "github": {
      "transport": {
        "type": "http",
        "url": "https://api.githubcopilot.com/mcp/"
      },
      "headers": {
        "Authorization": "Bearer ghp_YourGitHubTokenHere"
      },
      "description": "GitHub integration for issue/PR management (CRITICAL for ETEx)"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "description": "Structured problem-solving for complex tasks (CRITICAL for Design Agent)"
    },
    "context7": {
      "transport": {
        "type": "http",
        "url": "https://mcp.context7.com/mcp"
      },
      "headers": {
        "Authorization": "Bearer your_context7_api_key_here"
      },
      "description": "Latest library documentation for FastAPI, React, SQLAlchemy (HIGH PRIORITY)"
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "description": "E2E testing automation (Week 5-6)"
    },
    "duckduckgo": {
      "command": "node",
      "args": ["c:/path/to/servers/src/duckduckgo/index.js"],
      "description": "Web search for error solutions and examples (OPTIONAL)"
    }
  },
  "toolRules": {
    "Bash(cd:*)": "allow",
    "Bash(tree:*)": "allow",
    "Bash(ls:*)": "allow",
    "Bash(git status:*)": "allow",
    "Bash(git add:*)": "allow",
    "Bash(git commit:*)": "allow",
    "Bash(pytest:*)": "allow",
    "Read(**/docs/**)": "allow",
    "Read(**/.agents/**)": "allow",
    "Bash(rm:*)": "ask",
    "Bash(curl:*)": "ask"
  },
  "customInstructions": "Follow CLAUDE.md guidelines strictly. Use MCP servers when appropriate: GitHub for issues, Sequential Thinking for complex design, Context7 for latest library docs. All agents must coordinate through Issue Manager and follow 6-week MVP timeline."
}
```

---

## Verification Checklist

After installing all MCPs, verify each one:

### GitHub MCP
```
✅ "List open issues in ETEx repository"
✅ "Create a test issue with label type:test"
✅ "Close the test issue you just created"
```

### Sequential Thinking MCP
```
✅ "Use sequential thinking to break down: Design database schema for terms and synonyms"
✅ Expected: Step-by-step analysis with structured reasoning
```

### Context7 MCP
```
✅ "Get latest FastAPI file upload patterns using context7"
✅ "Show SQLAlchemy 2.0 async query examples using context7"
✅ Expected: Current documentation snippets (not outdated patterns)
```

### Playwright MCP (Week 5-6)
```
✅ "Take a screenshot of http://localhost:3000 using Playwright"
✅ Expected: Screenshot captured
```

### DuckDuckGo MCP (Optional)
```
✅ "Search for 'pytest async fixtures best practices' using DuckDuckGo"
✅ Expected: Recent search results
```

---

## Troubleshooting

### GitHub MCP: "Unauthorized" Error
**Problem**: Token invalid or insufficient scopes
**Solution**:
1. Regenerate GitHub PAT with correct scopes (repo, workflow, write:packages, read:org)
2. Update `.claude/settings.local.json` with new token
3. Restart Claude Code

### Sequential Thinking: Not Responding
**Problem**: MCP server not starting
**Solution**:
1. Ensure Node.js 18+ installed: `node --version`
2. Check network access to npmjs.org
3. Try manual install: `npx -y @modelcontextprotocol/server-sequential-thinking`

### Context7: Rate Limit Reached
**Problem**: Exceeded 100 requests/day
**Solution**:
1. Wait until next day (resets at midnight UTC)
2. Consider paid plan if frequent usage
3. Cache responses locally when possible

### Playwright: Browser Not Launching
**Problem**: Missing browser binaries
**Solution**:
```bash
npx playwright install
```

### DuckDuckGo: Connection Timeout
**Problem**: Network issues or server down
**Solution**:
1. Check internet connection
2. Try manual search to verify DuckDuckGo availability
3. Use Context7 or manual search as fallback

---

## Agent-Specific Usage Patterns

### Issue Manager Agent
```
Primary MCPs: GitHub, Sequential Thinking

Daily Usage:
- "Create Week 2 issue for PDF upload feature with high priority"
- "Use sequential thinking to verify issue #42 closure readiness"
- "List all blocked issues in current milestone"
```

### Design Agent
```
Primary MCPs: Context7, Sequential Thinking, GitHub

Daily Usage:
- "Use sequential thinking to design database schema for synonym linking"
- "Research latest SQLAlchemy relationship patterns using context7"
- "Create GitHub issue for spec: Feature 003 - Search API"
```

### Backend Expert Agent
```
Primary MCPs: Context7, Sequential Thinking, DuckDuckGo

Daily Usage:
- "Show latest FastAPI async session patterns using context7"
- "Use sequential thinking to analyze N+1 query prevention strategy"
- "Search for 'SQLAlchemy async connection pool settings' using DuckDuckGo"
```

### Frontend Expert Agent
```
Primary MCPs: Context7, Sequential Thinking, Playwright

Daily Usage:
- "Get latest MUI DataGrid virtualization patterns using context7"
- "Use sequential thinking to design bilingual term card component"
- "Test search UI responsiveness on mobile using Playwright" (Week 5-6)
```

### Project Manager Agent
```
Primary MCPs: GitHub, Sequential Thinking

Daily Usage:
- "Query Week 2 milestone progress using GitHub MCP"
- "Use sequential thinking to assess sprint velocity and risks"
- "Calculate completion percentage for current sprint"
```

### Coding Agent
```
Primary MCPs: GitHub, Context7, Playwright

Daily Usage:
- "Update issue #42 status to 'Implementation complete, ready for review'"
- "Verify vendor/glossary-app code is current using context7"
- "Run E2E test for PDF upload flow using Playwright" (Week 5-6)
```

### Testing Agent
```
Primary MCPs: Playwright, GitHub, Context7

Daily Usage:
- "Run E2E test suite using Playwright" (Week 5-6)
- "Create GitHub issue for failed test: test_term_search.py::test_pagination"
- "Get latest pytest-asyncio fixture patterns using context7"
```

### Review Coordinator Agent
```
Primary MCPs: GitHub, Sequential Thinking, Playwright

Daily Usage:
- "Post review report as PR comment on #123 using GitHub MCP"
- "Use sequential thinking to perform systematic security audit"
- "Verify accessibility compliance using Playwright" (Week 5-6)
```

---

## Next Steps After Installation

1. ✅ **Verify All MCPs**: Run verification commands above
2. ✅ **Update Agent CLAUDE.md Files**: Add MCP usage sections to all 8 agents
3. ✅ **Test Integration**: Have each agent use their primary MCPs
4. ✅ **Week 1 Start**: Begin using MCPs in daily workflows
5. ⏳ **Week 3 Review**: Assess if Apidog MCP should be added
6. ⏳ **Week 5 Install**: Add Playwright for E2E testing phase

---

## Missing MCPs (Identified by Agents)

Agents requested these MCPs that **don't exist yet** in the MCP ecosystem:

### High Priority Gaps
1. **Test Coverage Visualization MCP** - Requested by Testing, Review, Coding agents
2. **Database Query Analyzer MCP** - Requested by Backend Expert
3. **Storybook MCP** - Requested by Frontend Expert
4. **Code Quality MCP (Static Analysis)** - Requested by Review Coordinator

### Medium Priority Gaps
5. **Time Tracking MCP** (Harvest/Toggl) - Requested by Project Manager
6. **Slack/Discord Notifications MCP** - Requested by Project Manager
7. **CHANGELOG Generator MCP** - Requested by Issue Manager
8. **Linting/Formatting MCP** - Requested by Coding Agent
9. **Performance Testing MCP** (locust/k6) - Requested by Testing Agent
10. **Bundle Size Analyzer MCP** - Requested by Frontend Expert

**Note**: These don't exist yet. We documented them in the agent consultation summary for future reference. If they become available, we can add them.

---

## Expected Impact on ETEx Development

**With 5 Installed MCPs**:
- Issue creation time: 80% reduction (5 min → 1 min)
- Design decision quality: 30% improvement (structured thinking)
- Backend development velocity: 30% increase (latest docs)
- Frontend development velocity: 35% increase (latest docs)
- Sprint planning time: 40% reduction (automated GitHub queries)
- Test failure → issue time: 70% reduction (automated issue creation)
- Code review thoroughness: 25% improvement (systematic audits)
- Implementation → handoff time: 60% reduction (status updates)

**Overall Team Velocity Increase**: 40-50% (based on agent estimates)

---

## Security Reminders

- ✅ Store API keys in `.claude/settings.local.json` (gitignored)
- ❌ Never commit `.claude/settings.local.json` or `.claude/settings.json`
- ✅ Use `.claude/settings.template.json` for team sharing (no secrets)
- ✅ Rotate GitHub PAT every 90 days
- ✅ Use environment variables for CI/CD

---

## Support

- **Full MCP guide**: [docs/reference/mcp-server-integration.md](../reference/mcp-server-integration.md)
- **Agent feedback**: [.agents/outputs/mcp-agent-feedback-summary.md](../../.agents/outputs/mcp-agent-feedback-summary.md)
- **Quick setup**: [docs/getting-started/MCP-SETUP.md](MCP-SETUP.md)
- **Claude Code docs**: https://docs.claude.com/en/docs/claude-code/mcp

---

**Installation Guide Version**: 1.0
**Last Updated**: 2025-11-01
**Estimated Setup Time**: 20 minutes for all 5 MCPs
**Total Cost**: $0 (free tiers)
