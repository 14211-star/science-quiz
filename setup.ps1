<#
.SYNOPSIS
  DeepSeek V4 Pro - One-click Setup Script
.DESCRIPTION
  Installs Python packages, creates global config, copies skills, sets up .env
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File setup.ps1
#>

Write-Host "=== DeepSeek V4 Pro Setup ===" -ForegroundColor Cyan
Write-Host ""

# 1. Install Python packages
Write-Host "[1/4] Installing Python packages..." -ForegroundColor Yellow
python -m pip install httpx beautifulsoup4 python-dotenv supabase fastmcp -q
if ($?) { Write-Host "  ✅ Python packages installed" -ForegroundColor Green }
else { Write-Host "  ❌ Failed to install packages" -ForegroundColor Red }

# 2. Create global config directories
Write-Host "[2/4] Creating global config directories..." -ForegroundColor Yellow
$globalConfig = "$env:USERPROFILE\.config\opencode"
$globalSkills = "$globalConfig\skills"
@(
  "$globalConfig"
  "$globalSkills\web-search"
  "$globalSkills\file-reader"
  "$globalSkills\tailwind-default"
  "$globalSkills\auto-dispatcher"
  "$globalSkills\global-planner"
  "$globalSkills\code-evolver"
) | ForEach-Object {
  if (!(Test-Path $_)) { New-Item -ItemType Directory -Path $_ -Force | Out-Null }
}
Write-Host "  ✅ Directories created" -ForegroundColor Green

# 3. Copy skill files
Write-Host "[3/4] Copying skills to global..." -ForegroundColor Yellow
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillSrc = "$projectRoot\.opencode\skills"
if (Test-Path $skillSrc) {
  Copy-Item "$skillSrc\*" "$globalSkills\" -Recurse -Force
  Write-Host "  ✅ Skills copied to global" -ForegroundColor Green
} else {
  Write-Host "  ⚠️  No local skills directory found" -ForegroundColor Yellow
}

# 4. Create .env
Write-Host "[4/4] Setting up environment..." -ForegroundColor Yellow
if (!(Test-Path "$projectRoot\.env")) {
  if (Test-Path "$projectRoot\.env.example") {
    Copy-Item "$projectRoot\.env.example" "$projectRoot\.env"
    Write-Host "  ✅ .env created from .env.example" -ForegroundColor Green
    Write-Host "  ⚠️  Edit .env to add your API keys!" -ForegroundColor Yellow
  } else {
    Write-Host "  ⚠️  No .env.example found" -ForegroundColor Yellow
  }
} else {
  Write-Host "  ⏭️  .env already exists" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Edit .env with your API keys" -ForegroundColor Gray
Write-Host "  2. Start backend: python MCP/webui/server.py" -ForegroundColor Gray
Write-Host "  3. Open browser: http://localhost:3001" -ForegroundColor Gray
Write-Host "  4. Or use opencode desktop app (auto-loads global config)" -ForegroundColor Gray
Write-Host ""

# Verify
Write-Host "Verification:" -ForegroundColor Cyan
$files = @(
  "$projectRoot\MCP\deepseek_bridge.py"
  "$projectRoot\MCP\webui\server.py"
  "$projectRoot\MCP\webui\index.html"
  "$projectRoot\MCP\webui\app.js"
  "$projectRoot\MCP\gas\Code.gs"
)
$allOk = $true
foreach ($f in $files) {
  if (Test-Path $f) {
    Write-Host "  ✅ $f" -ForegroundColor Green
  } else {
    Write-Host "  ❌ $f" -ForegroundColor Red
    $allOk = $false
  }
}
if ($allOk) { Write-Host "`n🎉 All files verified!" -ForegroundColor Cyan }
