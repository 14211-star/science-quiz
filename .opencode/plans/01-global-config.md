# Plan 1/7: Global Config + Rules

## File: `~/.config/opencode/opencode.json`

Create this file at `C:\Users\ab117\.config\opencode\opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "web-search": {
      "type": "local",
      "command": ["uvx", "duckduckgo-mcp-server"],
      "enabled": true
    },
    "fetch": {
      "type": "local",
      "command": ["uvx", "mcp-server-fetch"],
      "enabled": true
    },
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\ab117\\OneDrive\\文件\\OPENCODE"],
      "enabled": true
    },
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "enabled": false,
      "environment": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "deepseek-bridge": {
      "type": "local",
      "command": ["python", "C:\\Users\\ab117\\OneDrive\\文件\\OPENCODE\\MCP\\deepseek_bridge.py"],
      "enabled": true,
      "environment": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_KEY": "${SUPABASE_KEY}",
        "GAS_WEBHOOK_URL": "${GAS_WEBHOOK_URL}",
        "GAS_API_KEY": "${GAS_API_KEY}"
      }
    }
  },
  "rules": [
    "Always use Tailwind CSS for all HTML/CSS/PPT work.",
    "Every answer must include: 1) Global overview 2) Implementation 3) Optimization."
  ],
  "tools": { "github_*": false }
}
```

## File: `~/.config/opencode/opencode.rules.md`

Create at `C:\Users\ab117\.config\opencode\opencode.rules.md`:

```markdown
# GPT-5.4 Global Thinking Rules

## Core Mandate
Before ANY response, ALWAYS:
1. Analyze the REAL goal behind the request
2. Auto-detect which MCP/SKILL tools are needed
3. Give a COMPLETE solution, not step-by-step
4. Include optimization + beautification suggestions

## Auto-Dispatch Table
| User Intent | Enable These |
|---|---|
| Current info / search | web-search + fetch MCPs |
| Code / files | filesystem MCP + file-reader skill |
| Database | deepseek-bridge (Supabase tools) |
| Cloud / webhook | deepseek-bridge (GAS tools) |
| HTML/CSS/PPT | tailwind-default skill |
| GitHub | github MCP |

## Output Format
1. **Global Overview** — 1 paragraph summary
2. **Analysis** — rationale, trade-offs, architecture
3. **Implementation** — complete code/config
4. **Optimization** — security, performance, beauty
5. **Evolution** — future scalability

## Security Rules
- Never expose secrets. Sanitize all paths. Validate all inputs.
- Parameterized queries only. Rate-limit public endpoints.
```

## File: `~/.config/opencode/skills/global-planner/SKILL.md`

```markdown
---
name: global-planner
description: Force global-first thinking - analyze the full picture before responding
license: MIT
compatibility: opencode
metadata:
  category: thinking
  priority: high
---

## What I do
Before responding to ANY request, enforce a global-analysis-first approach.

### Phase 1: Deep Analysis
- What is the user's REAL goal (not just surface request)?
- Constraints? (time, budget, tech stack)
- Related/adjacent problems?

### Phase 2: Solution Architecture
- Design the complete architecture
- Identify all components, dependencies, integrations
- Consider N+1 approaches, pick optimal

### Phase 3: Risk Assessment
- Security vulnerabilities, performance bottlenecks
- Maintenance burden, future extensibility

### Phase 4: Delivery
- Global overview first → then details → always optimization
```

## File: `~/.config/opencode/skills/code-evolver/SKILL.md`

```markdown
---
name: code-evolver
description: Auto-optimize, beautify, and secure every code change
license: MIT
compatibility: opencode
metadata:
  category: development
  priority: high
---

## What I do
Apply these automatically on every code create/modify:
- Naming conventions (PEP8, camelCase)
- Remove dead code, redundant comments
- Extract repeated logic into functions
- Path traversal prevention, input validation
- No secrets in code, parameterized queries
- Lazy imports, caching, async for I/O
- Consistent formatting, meaningful names
```

## File: `~/.config/opencode/skills/auto-dispatcher/SKILL.md`

```markdown
---
name: auto-dispatcher
description: Auto-analyze intent and enable/disable correct tools
license: MIT
compatibility: opencode
metadata:
  category: system
  priority: highest
---

## Intent-to-Tool Map
| Intent | Enable MCPs | Enable SKILLs |
|---|---|---|
| Search/info | web-search, fetch | web-search |
| Code/dev | filesystem | file-reader, code-evolver |
| Database | deepseek-bridge (Supabase) | — |
| Cloud/GAS | deepseek-bridge (GAS) | — |
| Design | — | tailwind-default |
| GitHub | github | — |
| General | none | global-planner |
```

## Apply Steps
1. Create directories: `mkdir -p ~\.config\opencode\skills\auto-dispatcher ~\.config\opencode\skills\global-planner ~\.config\opencode\skills\code-evolver`
2. Write each file above to its path
3. Restart opencode desktop app
