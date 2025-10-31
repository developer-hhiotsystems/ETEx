# Quick MCP Server Setup for ETEx

**Purpose**: Get essential MCP servers running in 15 minutes
**Prerequisite**: Claude Code installed and running
**Last Updated**: 2025-11-01

---

## Quick Start (3 Essential MCPs)

### 1. GitHub MCP ⭐ CRITICAL

**Install**:
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**Configure**:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: ✅ `repo`, ✅ `workflow`, ✅ `write:packages`, ✅ `read:org`
4. Copy token
5. When prompted, paste token as Authorization header

**Verify**:
```bash
claude mcp list
# Should show: github

claude mcp test github "List repositories"
```

**Usage**:
```
"Create Week 1 issue for database schema with labels type:feature,priority:high"
"Show all blocked issues in Week 2 milestone"
"List open PRs that modify CLAUDE.md"
```

---

### 2. Sequential Thinking MCP ⭐ CRITICAL

**Install**:
```bash
# Standard (macOS/Linux)
claude mcp add sequential-thinking npx -- -y @modelcontextprotocol/server-sequential-thinking

# Windows
claude mcp add sequential-thinking cmd -- /c npx -y @modelcontextprotocol/server-sequential-thinking
```

**No configuration needed** - works immediately!

**Verify**:
```bash
claude mcp list
# Should show: sequential-thinking

claude mcp test sequential-thinking "Break down: Design a REST API"
```

**Usage** (add to any prompt):
```
"Use sequential thinking to design the database schema for terms and synonyms"
"Think through this API endpoint design step by step"
"Analyze this architecture decision using sequential thinking"
```

---

### 3. Knowledge Graph Memory MCP ⭐ CRITICAL

**Prerequisites**:
- Node.js 18+ installed
- Git installed

**Install**:
```bash
# 1. Clone the memory server
git clone https://github.com/modelcontextprotocol/server-memory.git
cd server-memory
npm install
npm run build

# 2. Note the path (example: c:/dev/mcp-servers/server-memory)

# 3. Add to Claude Code (Windows example)
claude mcp add knowledge-graph node -- c:/dev/mcp-servers/server-memory/build/index.js

# 4. Set memory storage path
claude mcp update knowledge-graph -e MEMORY_PATH="c:/Users/developer/Documents/Coding Projects/ETEx/.agents/memory/"
```

**Create memory directory**:
```bash
mkdir -p "c:/Users/developer/Documents/Coding Projects/ETEx/.agents/memory/"
```

**Verify**:
```bash
claude mcp list
# Should show: knowledge-graph

# Test
claude mcp test knowledge-graph "Remember: ETEx uses 6-week MVP timeline"
```

**Usage**:
```
"Remember that we're using SQLAlchemy 2.0 with async patterns"
"Recall the code reuse strategy from vendor/glossary-app"
"What do you remember about the Issue Manager agent?"
```

---

## Verify All 3 MCPs Working

```bash
# List all installed MCPs
claude mcp list

# Expected output:
# github (http transport)
# sequential-thinking (npx)
# knowledge-graph (node)
```

**Quick test**:
```
Ask Claude Code: "List all installed MCP servers and test each one"
```

---

## Next Steps (Optional - Week 1+)

### 4. Context7 MCP (Latest Library Docs)

**Install**:
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
```

**Configure**:
1. Go to https://context7.com and sign up (free tier: 100 requests/day)
2. Get API key from dashboard
3. When prompted, enter API key as Authorization header

**Usage**:
```
"Show latest FastAPI async patterns using context7"
"Generate SQLAlchemy 2.0 query example using context7"
```

---

### 5. DuckDuckGo MCP (Web Search - No API Key!)

**Install**:
```bash
# 1. Clone MCP servers repo
git clone https://github.com/modelcontextprotocol/servers.git
cd servers/src/duckduckgo
npm install

# 2. Add to Claude Code
claude mcp add duckduckgo node -- c:/path/to/servers/src/duckduckgo/index.js
```

**Usage**:
```
"Search for SQLAlchemy N+1 query prevention examples"
"Find latest spaCy German NLP tutorials"
```

---

## Troubleshooting

### GitHub MCP "Unauthorized" error
- Check token has correct scopes (repo, workflow)
- Token may have expired - generate new one
- Verify token in Authorization header: `Bearer YOUR_TOKEN`

### Sequential Thinking not responding
- Ensure you include trigger phrase: "use sequential thinking"
- Check installation: `claude mcp list`
- Try: `claude mcp remove sequential-thinking` then reinstall

### Knowledge Graph Memory not persisting
- Check memory directory exists: `ls .agents/memory/`
- Verify MEMORY_PATH environment variable set
- Check permissions: directory must be writable

### "MCP server not found"
- Run: `claude mcp list` to see installed servers
- Check spelling matches exactly
- Restart Claude Code after installing new MCP

---

## Configuration File Method (Alternative)

Instead of installing via CLI, you can configure in `.claude/settings.local.json`:

```bash
# 1. Copy template
cp .claude/settings.template.json .claude/settings.local.json

# 2. Edit file and add your API keys/paths
# Replace:
#   YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
#   YOUR_CONTEXT7_API_KEY
#   PATH_TO_MEMORY_SERVER
#   PATH_TO_SERVERS

# 3. Restart Claude Code
```

See [.claude/README.md](../../.claude/README.md) for detailed configuration instructions.

---

## What's Next?

After installing MCPs, you can:

1. **Start Week 1** - Database schema design
   - Use Sequential Thinking for schema design
   - Use GitHub MCP to create Week 1 issues
   - Memory MCP retains decisions across sessions

2. **Test Agent Integration**
   - Ask Design Agent to create a spec using sequential thinking
   - Have Issue Manager create a GitHub issue
   - Verify Knowledge Graph remembers context

3. **Explore MCP Ecosystem**
   - Install MCP Compass to discover more servers
   - Add Context7 when you need latest library docs
   - Add Playwright for E2E testing in Week 5-6

---

## Support

- **Full MCP integration guide**: [docs/reference/mcp-server-integration.md](../reference/mcp-server-integration.md)
- **Claude Code docs**: https://docs.claude.com/en/docs/claude-code/mcp
- **.claude/ config help**: [.claude/README.md](../../.claude/README.md)

---

**Estimated Setup Time**: 15 minutes for all 3 essential MCPs
**Cost**: $0 (all free)
**Benefit**: 20%+ productivity increase from reduced context switching

---

**Last Updated**: 2025-11-01
**Next Review**: Before Week 1 sprint planning
