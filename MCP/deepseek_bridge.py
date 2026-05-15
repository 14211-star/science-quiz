import os
import json
import hashlib
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote

mcp = FastMCP("deepseek-bridge", description="DeepSeek Bridge - Smart MCP Server")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── Helpers ──────────────────────────────────────────────────────────────────

def _safe_path(user_path: str) -> Optional[Path]:
    target = (PROJECT_ROOT / user_path).resolve()
    try:
        target.relative_to(PROJECT_ROOT)
    except ValueError:
        return None
    return target if target.exists() else None

def _get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)

# ── Intent Detection ─────────────────────────────────────────────────────────

@mcp.tool()
async def auto_detect_intent(user_request: str) -> str:
    """Analyze a user request and return which tools/MCPs are needed."""
    text = user_request.lower()
    tools = []

    keywords_search = ["search", "查", "找", "google", "news", "最新", "what is", "how to", "find", "look up"]
    keywords_code = ["code", "file", "read", "寫", "改", "修", "程式", "檔案", "讀取"]
    keywords_db = ["save", "store", "database", "查詢", "存", "資料庫", "supabase"]
    keywords_cloud = ["webhook", "gas", "google app", "sheet", "trigger"]
    keywords_design = ["html", "css", "ppt", "tailwind", "design", "ui", "style", "佈局"]
    keywords_github = ["github", "git", "pr", "issue", "repo", "commit", "push"]

    if any(k in text for k in keywords_search): tools.append("web-search + fetch")
    if any(k in text for k in keywords_code): tools.append("filesystem + file-reader")
    if any(k in text for k in keywords_db): tools.append("deepseek-bridge (Supabase)")
    if any(k in text for k in keywords_cloud): tools.append("deepseek-bridge (GAS)")
    if any(k in text for k in keywords_design): tools.append("tailwind-default")
    if any(k in text for k in keywords_github): tools.append("github")
    if not tools: tools.append("global-planner (general chat)")

    return f"## Auto-Detected Tools\n" + "\n".join("- " + t for t in tools)

# ── Web Search ───────────────────────────────────────────────────────────────

@mcp.tool()
async def smart_search(query: str, context: str = "", max_results: int = 5) -> str:
    """Context-aware web search. Provide context to auto-improve the query."""
    if context:
        query = f"{query} ({context})"
    return await web_search(query, max_results)


@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo. Returns JSON with titles, URLs, snippets."""
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        resp = await client.post(url, headers=headers, data={"q": query})
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for selector in [".result", ".web-result", "article", ".results-item"]:
        items = soup.select(selector)
        if items:
            break
    else:
        items = []

    for item in items[:max_results]:
        title_el = None
        for link_sel in [".result__title a", "a[href]", "h2 a", ".title a"]:
            title_el = item.select_one(link_sel)
            if title_el and title_el.get("href"):
                break
        snippet_el = item.select_one(".result__snippet") or item.select_one(".snippet") or item.select_one("p")
        if title_el:
            results.append({
                "title": title_el.get_text(strip=True),
                "url": title_el.get("href", ""),
                "snippet": snippet_el.get_text(strip=True) if snippet_el else ""
            })

    if not results:
        return json.dumps([{"title": "No results found", "url": "", "snippet": ""}])
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
async def fetch_page(url: str) -> str:
    """Fetch and extract text content from a web page (max 300 lines)."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [l for l in text.splitlines() if l.strip()]
    return "\n".join(lines[:300])

# ── Filesystem ───────────────────────────────────────────────────────────────

@mcp.tool()
async def read_project_files(extension: str = "") -> str:
    """Recursively list all project files, optionally filtered by extension (e.g. '.py')."""
    results = []
    for path in sorted(PROJECT_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if extension and path.suffix != extension:
            continue
        try:
            rel = path.relative_to(PROJECT_ROOT)
            results.append(f"{rel} ({path.stat().st_size} bytes)")
        except (ValueError, OSError):
            pass
    return "\n".join(results) if results else "No files found."


@mcp.tool()
async def read_file(file_path: str) -> str:
    """Read a text file (path relative to project root). Path traversal protected."""
    target = _safe_path(file_path)
    if target is None:
        return "Error: Invalid path (path traversal detected or file not found)"
    try:
        content = target.read_text(encoding="utf-8")
        lines = content.splitlines()
        if len(lines) > 500:
            content = "\n".join(lines[:500]) + f"\n\n... (truncated, {len(lines)} total lines)"
        return f"```\n{content}\n```"
    except UnicodeDecodeError:
        return "Error: Binary file or unsupported encoding."


@mcp.tool()
async def batch_read_files(patterns: str) -> str:
    """Read multiple files at once. patterns: comma-separated paths relative to root."""
    paths = [p.strip() for p in patterns.split(",")]
    results = []
    for p in paths:
        target = _safe_path(p)
        if target is None:
            results.append(f"## {p}\nError: Invalid or not found")
        else:
            try:
                content = target.read_text(encoding="utf-8")
                results.append(f"## {p}\n```\n{content[:3000]}\n```")
            except UnicodeDecodeError:
                results.append(f"## {p}\nError: Binary file")
    return "\n\n".join(results)


@mcp.tool()
async def project_analyzer() -> str:
    """Analyze project structure and give optimization suggestions."""
    stats = {"files": 0, "py": 0, "js": 0, "html": 0, "css": 0, "json": 0, "dirs": set()}
    large_files = []

    for path in PROJECT_ROOT.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            stats["files"] += 1
            ext = path.suffix.lower()
            if ext in stats:
                stats[ext] += 1
            stats["dirs"].add(path.parent)
            try:
                sz = path.stat().st_size
                if sz > 100000:
                    large_files.append(f"  - {path.relative_to(PROJECT_ROOT)} ({sz//1000}KB)")
            except OSError:
                pass

    lines = [
        "## Project Analysis",
        f"- Total files: {stats['files']}",
        f"- Directories: {len(stats['dirs'])}",
        f"- Python files: {stats.get('.py', 0)}",
        f"- JS files: {stats.get('.js', 0)}",
        f"- HTML files: {stats.get('.html', 0)}",
        f"- CSS files: {stats.get('.css', 0)}",
        f"- JSON files: {stats.get('.json', 0)}",
    ]
    if large_files:
        lines.append("\n## Large Files (>100KB)")
        lines.extend(large_files)

    checks = [
        (".env", "No .env file found (create from .env.example)"),
        (".gitignore", ".gitignore exists"),
        ("AGENTS.md", "AGENTS.md exists"),
        ("opencode.json", "opencode.json exists"),
    ]
    lines.append("\n## Config Checks")
    for fname, msg in checks:
        ok = (PROJECT_ROOT / fname).exists()
        lines.append(f"- {'✅' if ok else '❌'} {msg}")

    return "\n".join(lines)


@mcp.tool()
async def code_beautifier(file_path: str) -> str:
    """Analyze a code file and return beautification/optimization suggestions."""
    target = _safe_path(file_path)
    if target is None:
        return "Error: Invalid path"
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "Error: Binary file"

    lines = content.splitlines()
    suggestions = []
    ext = target.suffix

    if ext == ".py":
        try:
            import ast
            ast.parse(content)
            suggestions.append("✅ Valid Python syntax")
        except SyntaxError as e:
            suggestions.append(f"❌ Syntax error: {e}")

        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                suggestions.append(f"⚠️ Line {i}: too long ({len(line)} chars, max 100)")
            if line.strip().startswith("print("):
                suggestions.append(f"💡 Line {i}: consider using logging instead of print()")
    elif ext == ".js":
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                suggestions.append(f"⚠️ Line {i}: too long ({len(line)} chars)")

    total_lines = len(lines)
    total_chars = sum(len(l) for l in lines)
    suggestions.append(f"\n📊 Stats: {total_lines} lines, {total_chars} chars")

    return "\n".join(suggestions)

# ── Supabase ─────────────────────────────────────────────────────────────────

@mcp.tool()
async def supabase_query(sql: str) -> str:
    """Execute SQL via Supabase. Requires SUPABASE_URL and SUPABASE_KEY."""
    url = _get_env("SUPABASE_URL")
    key = _get_env("SUPABASE_KEY")
    if not url or not key:
        return "Error: SUPABASE_URL and SUPABASE_KEY not set."

    rest_url = f"{url.rstrip('/')}/rest/v1/rpc/query"
    headers = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(rest_url, json={"query": sql}, headers=headers)

    if resp.status_code == 200:
        return json.dumps(resp.json(), indent=2, ensure_ascii=False)
    return f"Error ({resp.status_code}): {resp.text[:500]}"


@mcp.tool()
async def supabase_select(table: str, select_cols: str = "*", limit: int = 100) -> str:
    """Select rows (read-only, safe for anon key)."""
    url = _get_env("SUPABASE_URL")
    key = _get_env("SUPABASE_KEY")
    if not url or not key:
        return "Error: SUPABASE_URL and SUPABASE_KEY not set."

    rest_url = f"{url.rstrip('/')}/rest/v1/{table}?select={select_cols}&limit={limit}"
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(rest_url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        return json.dumps(data, indent=2, ensure_ascii=False) if data else "No rows found."
    return f"Error ({resp.status_code}): {resp.text[:500]}"

# ── Google Apps Script ───────────────────────────────────────────────────────

@mcp.tool()
async def gas_trigger(endpoint: str, payload: str = "{}") -> str:
    """Call GAS webhook with API key authentication."""
    base_url = _get_env("GAS_WEBHOOK_URL")
    api_key = _get_env("GAS_API_KEY")
    if not base_url:
        return "Error: GAS_WEBHOOK_URL not set."

    full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-Api-Key"] = api_key

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return "Error: Invalid JSON payload."

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(full_url, json=data, headers=headers)

    return f"Status: {resp.status_code}\n{resp.text[:2000]}"

# ── Entry ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
