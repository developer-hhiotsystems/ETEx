# Claude Code Configuration for ETEx

**Purpose**: MCP server configuration and Claude Code settings
**Last Updated**: 2025-11-01

---

## Files in This Directory

### settings.template.json ✅ COMMITTED
Template for MCP server configuration. **DO NOT** add your API keys here.

### settings.local.json ❌ GITIGNORED
Your personal MCP configuration with API keys. **NEVER** commit this file.

### settings.json ❌ GITIGNORED
Alternative location for MCP configuration. **NEVER** commit this file.

---

## Setup Instructions

### 1. Copy Template to Local Settings

```bash
# From ETEx root directory
cp .claude/settings.template.json .claude/settings.local.json
```

### 2. Add Your API Keys

Edit `.claude/settings.local.json` and replace placeholders:

- `YOUR_GITHUB_PERSONAL_ACCESS_TOKEN` - Get from https://github.com/settings/tokens
  - Required scopes: `repo`, `workflow`, `write:packages`, `read:org`

- `YOUR_CONTEXT7_API_KEY` - Get from https://context7.com (free tier available)

- `PATH_TO_MEMORY_SERVER` - Path where you cloned the memory server
  - Example: `c:/dev/mcp-servers/server-memory`

- `PATH_TO_SERVERS` - Path where you cloned the MCP servers repo
  - Example: `c:/dev/mcp-servers/servers`

### 3. Verify Configuration

```bash
# List installed MCP servers
claude mcp list

# Should show:
# - github
# - sequential-thinking
# - knowledge-graph
# - context7 (if API key configured)
# - duckduckgo
# - playwright
# - apidog
```

### 4. Test MCP Servers

```bash
# Test GitHub MCP
claude mcp test github "List open issues"

# Test Sequential Thinking
claude mcp test sequential-thinking "Break down: Design database schema"

# Test Context7 (if configured)
claude mcp test context7 "Get FastAPI documentation"
```

---

## Priority Installation Order

### Week 0 (Before Development)
1. ✅ GitHub MCP - Essential for issue management
2. ✅ Sequential Thinking MCP - Critical for design work
3. ✅ Knowledge Graph Memory MCP - Retain context

### Week 1-2 (Backend Setup)
4. Context7 MCP - Latest FastAPI/SQLAlchemy docs
5. DuckDuckGo MCP - Error solutions

### Week 3-4 (API Development)
6. Apidog MCP - API spec validation

### Week 5-6 (Frontend & Testing)
7. Playwright MCP - E2E testing

---

## Security Best Practices

### ✅ DO:
- Store API keys in `.claude/settings.local.json`
- Use environment variables for CI/CD
- Rotate GitHub PAT every 90 days
- Keep template file updated when adding new MCPs

### ❌ DON'T:
- Commit `.claude/settings.local.json` or `.claude/settings.json`
- Share your API keys in Slack/email/GitHub issues
- Use production API keys in development
- Commit any file containing `Bearer` tokens

---

## MCP Server Documentation

**Complete setup guide**: [docs/reference/mcp-server-integration.md](../docs/reference/mcp-server-integration.md)

**Agent-specific usage**: See root [CLAUDE.md](../CLAUDE.md) section "MCP Server Integration"

---

## Troubleshooting

### GitHub MCP not connecting
```bash
# Check token scopes
gh auth status

# Regenerate token with correct scopes
# Go to: https://github.com/settings/tokens
# Scopes: repo, workflow, write:packages, read:org
```

### Sequential Thinking not activating
- Ensure you include "use sequential thinking" in your prompt
- Verify installation: `claude mcp list`
- Check command: `npx -y @modelcontextprotocol/server-sequential-thinking`

### Context7 rate limit reached
- Free tier: 100 requests/day
- Upgrade to paid plan: https://context7.com/pricing
- Cache responses when possible

### Knowledge Graph Memory errors
```bash
# Check memory directory exists
mkdir -p .agents/memory/

# Check disk space
df -h .agents/memory/

# Clear old memories if needed (careful!)
rm -rf .agents/memory/old/*
```

### Apidog OpenAPI spec not found
```bash
# Ensure FastAPI app is running
cd src/backend
uvicorn main:app --reload

# Check OpenAPI spec accessible
curl http://localhost:8000/openapi.json

# Update Apidog MCP config with correct URL
```

---

## Environment-Specific Configurations

### Development (Local)
Use `.claude/settings.local.json` with:
- GitHub PAT with repo scope
- Context7 free tier API key
- Local memory storage path

### CI/CD (GitHub Actions)
Use environment variables:
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  CONTEXT7_API_KEY: ${{ secrets.CONTEXT7_API_KEY }}
```

### Team Sharing
- Share `.claude/settings.template.json` (no secrets)
- Each developer creates their own `.claude/settings.local.json`
- Document any new MCPs in template + README

---

## Adding New MCP Servers

1. **Research** - Find MCP server in ecosystem
2. **Test locally** - Install and verify functionality
3. **Update template** - Add to `settings.template.json` with placeholder
4. **Update documentation**:
   - Add to [docs/reference/mcp-server-integration.md](../docs/reference/mcp-server-integration.md)
   - Update this README troubleshooting section
   - Update root CLAUDE.md if agent-specific
5. **Commit template** - Template only, not your local settings!

---

## Support

- **Claude Code docs**: https://docs.claude.com/en/docs/claude-code
- **MCP ecosystem**: Use MCP Compass to discover servers
- **ETEx-specific help**: See [docs/reference/mcp-server-integration.md](../docs/reference/mcp-server-integration.md)

---

**Last Updated**: 2025-11-01
**Maintained By**: Project Manager Agent
