# Plan 7/7: setup.ps1 + .env.example + Summary

## File: `setup.ps1`

**Path:** `C:\Users\ab117\OneDrive\文件\OPENCODE\setup.ps1`

```powershell
# DeepSeek V4 Pro - One-click Setup Script
# Run: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "=== DeepSeek V4 Pro Setup ===" -ForegroundColor Cyan

# 1. Install Python packages
Write-Host "[1/4] Installing Python packages..." -ForegroundColor Yellow
python -m pip install httpx beautifulsoup4 python-dotenv supabase fastmcp -q
Write-Host "  ✅ Python packages installed" -ForegroundColor Green

# 2. Create global config directories
Write-Host "[2/4] Creating global config directories..." -ForegroundColor Yellow
$globalConfig = "$env:USERPROFILE\.config\opencode"
$globalSkills = "$globalConfig\skills"
@(
  "$globalConfig",
  "$globalSkills\web-search",
  "$globalSkills\file-reader",
  "$globalSkills\tailwind-default",
  "$globalSkills\auto-dispatcher",
  "$globalSkills\global-planner",
  "$globalSkills\code-evolver"
) | ForEach-Object {
  if (!(Test-Path $_)) { New-Item -ItemType Directory -Path $_ -Force | Out-Null }
}
Write-Host "  ✅ Directories created" -ForegroundColor Green

# 3. Copy config files
Write-Host "[3/4] Copying config and skill files..." -ForegroundColor Yellow
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item "$projectRoot\.opencode\skills\*" "$globalSkills\" -Recurse -Force
Write-Host "  ✅ Skills copied to global" -ForegroundColor Green

# 4. Create .env if not exists
Write-Host "[4/4] Setting up environment..." -ForegroundColor Yellow
if (!(Test-Path "$projectRoot\.env")) {
  Copy-Item "$projectRoot\.env.example" "$projectRoot\.env"
  Write-Host "  ✅ .env created (edit it to add your API keys)" -ForegroundColor Green
} else {
  Write-Host "  ⏭️ .env already exists" -ForegroundColor Yellow
}

# Summary
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "  1. Edit .env with your API keys"
Write-Host "  2. Start backend: python MCP/webui/server.py"
Write-Host "  3. Open browser: http://localhost:3001"
Write-Host "  4. Or use opencode desktop app (auto-loads global config)`n"
```

## File: `.env.example` (updated)

**Path:** `C:\Users\ab117\OneDrive\文件\OPENCODE\.env.example`

```env
# DeepSeek API (required)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Web UI Backend
WEBUI_HOST=0.0.0.0
WEBUI_PORT=3001

# Supabase (optional)
SUPABASE_URL=
SUPABASE_KEY=

# Google Apps Script (optional)
GAS_WEBHOOK_URL=
GAS_API_KEY=
```

## Summary: All Files Changed (7 files)

| # | File | Action | Reason |
|---|------|--------|--------|
| 1 | `~/.config/opencode/opencode.json` | **NEW** | Global MCP config (all projects) |
| 2 | `~/.config/opencode/opencode.rules.md` | **NEW** | Global system prompt rules |
| 3 | `~/.config/opencode/skills/auto-dispatcher/SKILL.md` | **NEW** | Auto intent-to-tool mapping |
| 4 | `~/.config/opencode/skills/global-planner/SKILL.md` | **NEW** | Global-first thinking |
| 5 | `~/.config/opencode/skills/code-evolver/SKILL.md` | **NEW** | Auto code optimization |
| 6 | `MCP/deepseek_bridge.py` | **REWRITE** | Security fixes + smart features |
| 7 | `MCP/gas/Code.gs` | **REWRITE** | API key + whitelist + rate limit |
| 8 | `MCP/webui/server.py` | **REWRITE** | Rate limit + streaming + security |
| 9 | `MCP/webui/index.html` | **REWRITE** | GPT-5.4 glassmorphism UI + Tailwind |
| 10 | `MCP/webui/app.js` | **REWRITE** | Markdown + thinking chain + tools UI |
| 11 | `setup.ps1` | **NEW** | One-click setup script |

## To Apply

1. Remove the edit deny permission in your opencode config
2. Or manually copy each file from the plan files above to its target path
3. Run `setup.ps1` or manually apply changes individually
