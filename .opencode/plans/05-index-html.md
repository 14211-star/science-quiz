# Plan 5/7: Web UI index.html (GPT-5.4 Style + Tailwind)

**Path:** `C:\Users\ab117\OneDrive\文件\OPENCODE\MCP\webui\index.html`

## Features
- ✅ Tailwind CDN + custom config
- ✅ GPT-5.4 dark theme (glassmorphism)
- ✅ Thinking chain collapse panel (show AI's reasoning)
- ✅ Tool usage indicators (real-time icons)
- ✅ Markdown rendering via marked.js
- ✅ File drag-and-drop zone
- ✅ One-click optimization button

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DeepSeek V4 Pro</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            glass: { DEFAULT: 'rgba(30,30,46,0.85)', border: 'rgba(255,255,255,0.08)' },
            surface: '#0F0F1A',
            panel: '#1A1A2E',
          }
        }
      }
    }
  </script>
  <style>
    * { scrollbar-width: thin; scrollbar-color: #3B3B5C transparent; }
    .glass { background: rgba(26,26,46,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.06); }
    .thinking-enter { animation: slideDown 0.3s ease-out; }
    @keyframes slideDown { from { opacity: 0; max-height: 0; } to { opacity: 1; max-height: 500px; } }
    .typing-dots::after { content: ''; animation: dots 1.5s steps(4,end) infinite; }
    @keyframes dots { 0%,20%{content:''} 40%{content:'.'} 60%{content:'..'} 80%,100%{content:'...'} }
    .msg-in { animation: fadeIn 0.3s ease-out; }
    @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    .markdown-body h1, .markdown-body h2, .markdown-body h3 { color: #A5B4FC; margin-top: 1em; margin-bottom: 0.5em; }
    .markdown-body p { margin: 0.5em 0; line-height: 1.6; }
    .markdown-body pre { background: #0F0F1A; border-radius: 8px; padding: 12px; overflow-x: auto; margin: 8px 0; border: 1px solid rgba(255,255,255,0.06); }
    .markdown-body code { font-size: 0.85em; }
    .markdown-body ul, .markdown-body ol { padding-left: 1.5em; margin: 0.5em 0; }
    .markdown-body a { color: #818CF8; text-decoration: underline; }
    .markdown-body blockquote { border-left: 3px solid #6366F1; padding-left: 12px; color: #9CA3AF; margin: 8px 0; }
  </style>
</head>
<body class="bg-surface text-gray-100 h-screen flex flex-col dark overflow-hidden">
  <header class="glass border-b border-glass-border px-6 py-3 flex items-center justify-between flex-shrink-0">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center text-lg font-bold shadow-lg shadow-indigo-500/20">DS</div>
      <div>
        <h1 class="text-lg font-semibold bg-gradient-to-r from-indigo-300 to-purple-300 bg-clip-text text-transparent">DeepSeek V4 Pro</h1>
        <p class="text-xs text-gray-500">全局思維 · 自動工具調度</p>
      </div>
    </div>
    <div class="flex items-center gap-4">
      <button id="optimizeBtn" class="px-3 py-1.5 text-xs bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 rounded-lg transition-all shadow-lg shadow-emerald-600/20">✨ 全局優化</button>
      <div class="flex items-center gap-2 text-xs text-gray-500">
        <span id="toolIndicator" class="flex items-center gap-1.5 px-2 py-1 rounded-full bg-panel border border-glass-border">
          <span class="w-1.5 h-1.5 rounded-full bg-gray-500"></span> 待命
        </span>
      </div>
    </div>
  </header>

  <div class="flex-1 flex overflow-hidden">
    <aside class="w-64 glass border-r border-glass-border p-4 flex flex-col gap-3 hidden md:flex flex-shrink-0">
      <button id="newChatBtn" class="w-full py-2 px-3 bg-indigo-600/80 hover:bg-indigo-500 rounded-lg text-sm font-medium transition-all">＋ 新對話</button>
      <div class="text-xs text-gray-500 uppercase tracking-wider mt-2">歷史記錄</div>
      <div id="historyList" class="flex-1 overflow-y-auto space-y-1 text-sm">
        <div class="text-gray-600 text-center py-8">尚無記錄</div>
      </div>
    </aside>

    <main class="flex-1 flex flex-col min-w-0">
      <div id="messages" class="flex-1 overflow-y-auto px-4 md:px-8 py-4 space-y-4"></div>

      <div class="glass border-t border-glass-border px-4 md:px-8 py-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-end gap-2">
            <textarea id="userInput" rows="1" placeholder="輸入訊息... (Enter 發送, Shift+Enter 換行)" class="flex-1 bg-panel/50 border border-glass-border rounded-xl px-4 py-3 text-sm outline-none focus:border-indigo-500/50 transition-colors placeholder-gray-600 resize-none"></textarea>
            <button id="sendBtn" class="p-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 rounded-xl transition-all disabled:cursor-not-allowed shadow-lg shadow-indigo-600/20" disabled>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19V5m0 0l-7 7m7-7l7 7"/></svg>
            </button>
          </div>
          <div id="toolbar" class="flex gap-4 mt-2 text-xs text-gray-500">
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-indigo-400 transition-colors">
              <input type="checkbox" id="searchToggle" class="accent-indigo-500" checked> <span>🔍 搜尋</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-indigo-400 transition-colors">
              <input type="checkbox" id="fileReadToggle" class="accent-indigo-500"> <span>📁 讀檔</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-indigo-400 transition-colors">
              <input type="checkbox" id="thinkToggle" class="accent-indigo-500" checked> <span>🧠 思維鏈</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer hover:text-indigo-400 transition-colors ml-auto">
              <input type="file" id="fileUpload" class="hidden" accept=".txt,.py,.js,.html,.css,.json,.md,.csv,.pdf,.docx">
              <span>📎 附件</span>
            </label>
          </div>
        </div>
      </div>
    </main>
  </div>

  <script src="app.js"></script>
</body>
</html>
```
