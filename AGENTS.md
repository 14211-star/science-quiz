# OpenCode Project Rules

## HTML/CSS & PPT
- Default to **Tailwind CSS** for all HTML/CSS pages and PPT presentations.
- Use CDN (`<script src="https://cdn.tailwindcss.com">`) for simple pages.
- For presentations, combine Tailwind CSS with Reveal.js or Slidev.

## Superpowers (installed)
- 14 development workflow skills (brainstorming, TDD, code review, debugging, etc.)
- Use `skill` tool to load any Superpowers skill by name

## Python HTTP Server Rules
- Always call `self.send_response(status)` BEFORE any `self.send_header()` calls
- Always include `Content-Length` header with the byte length of the response body
- Order: `send_response` → `send_header(s)` → `end_headers` → `wfile.write(body)`
- Never call `send_header` before `send_response` (causes ERR_INVALID_HTTP_RESPONSE)
