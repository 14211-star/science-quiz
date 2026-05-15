const API_BASE = 'http://localhost:3001';

const $ = id => document.getElementById(id);
const messagesEl = $('messages');
const inputEl = $('userInput');
const sendBtn = $('sendBtn');
const searchToggle = $('searchToggle');
const fileReadToggle = $('fileReadToggle');
const thinkToggle = $('thinkToggle');
const optimizeBtn = $('optimizeBtn');
const newChatBtn = $('newChatBtn');
const toolIndicator = $('toolIndicator');
const fileUpload = $('fileUpload');

let conversation = [];

// ── Input auto-resize ────────────────────────────────────────────────────────
inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = Math.min(inputEl.scrollHeight, 200) + 'px';
  sendBtn.disabled = !inputEl.value.trim();
});
inputEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (inputEl.value.trim()) sendMessage(); }
});
sendBtn.addEventListener('click', sendMessage);
newChatBtn.addEventListener('click', () => { conversation = []; renderMessages(); });

// ── File upload ──────────────────────────────────────────────────────────────
fileUpload.addEventListener('change', async e => {
  const file = e.target.files[0];
  if (!file) return;
  const text = await file.text();
  conversation.push({
    role: 'user',
    content: `[Uploaded: ${file.name}]\n\`\`\`\n${text.slice(0, 10000)}\n\`\`\``
  });
  renderMessages();
});

// ── Send message ─────────────────────────────────────────────────────────────
async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  conversation.push({ role: 'user', content: text });
  inputEl.value = ''; inputEl.style.height = 'auto'; sendBtn.disabled = true;
  renderAndScroll();

  const assistantMsg = { role: 'assistant', content: '', loading: true, sources: [], tools: {} };
  conversation.push(assistantMsg);
  setToolIndicator('處理中', 'yellow');
  renderAndScroll();

  try {
    const resp = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        search_enabled: searchToggle.checked,
        file_read_enabled: fileReadToggle.checked,
        history: conversation.filter(m => !m.loading)
      })
    });
    const data = await resp.json();
    assistantMsg.content = data.reply || '（無回應）';
    assistantMsg.loading = false;
    assistantMsg.sources = data.sources || [];
    assistantMsg.files_read = data.files_read || [];
    assistantMsg.tools = data.tools_used || {};

    if (data.tools_used?.search) setToolIndicator('搜尋完成', 'green');
    else if (data.tools_used?.file_read) setToolIndicator('讀檔完成', 'green');
    else setToolIndicator('完成', 'green');
  } catch (err) {
    assistantMsg.content = '⚠️ 連線錯誤：無法連接到後端伺服器';
    assistantMsg.loading = false;
    setToolIndicator('離線', 'red');
  }
  renderAndScroll();
}

// ── Render messages ──────────────────────────────────────────────────────────
function renderMessages() {
  messagesEl.innerHTML = conversation.map((msg, i) => {
    if (msg.role === 'user') {
      return `<div class="msg-in flex justify-end">
        <div class="max-w-[80%] bg-indigo-600/80 rounded-2xl rounded-br-lg px-4 py-2.5 text-sm shadow-lg shadow-indigo-600/10">${escHtml(msg.content).replace(/\n/g, '<br>')}</div>
      </div>`;
    }
    return `<div class="msg-in flex justify-start gap-3">
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 via-purple-500 to-pink-500 flex-shrink-0 flex items-center justify-center text-xs font-bold shadow-lg shadow-purple-500/20">DS</div>
      <div class="max-w-[80%] space-y-2">
        ${msg.loading ? renderLoading() : renderAssistant(msg)}
      </div>
    </div>`;
  }).join('');
}

function renderLoading() {
  return `<div class="glass rounded-2xl rounded-bl-lg px-4 py-3 text-sm">
    <div class="flex items-center gap-2">
      <div class="flex gap-1"><span class="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style="animation-delay:0s"></span><span class="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style="animation-delay:0.2s"></span><span class="w-2 h-2 rounded-full bg-pink-400 animate-bounce" style="animation-delay:0.4s"></span></div>
      <span class="text-gray-400 text-xs">思考中...</span>
    </div>
  </div>`;
}

function renderAssistant(msg) {
  const showThink = thinkToggle.checked;
  const md = marked.parse(msg.content || '');
  let html = `<div class="glass rounded-2xl rounded-bl-lg px-4 py-3 text-sm markdown-body">${md}</div>`;

  if (showThink && (msg.sources?.length || msg.files_read?.length || Object.keys(msg.tools).length)) {
    const toolsUsed = [];
    if (msg.tools?.search) toolsUsed.push('🔍 網路搜尋');
    if (msg.tools?.file_read) toolsUsed.push('📁 檔案讀取');
    if (msg.files_read?.length) toolsUsed.push(...msg.files_read.map(f => `📄 ${f}`));

    html += `<details class="thinking-enter mt-2">
      <summary class="text-xs text-gray-500 cursor-pointer hover:text-indigo-400 transition-colors select-none">🧠 使用工具 (${toolsUsed.length})</summary>
      <div class="mt-1 space-y-1">`;
    toolsUsed.forEach(t => { html += `<div class="text-xs text-gray-400">${t}</div>`; });
    if (msg.sources?.length) {
      html += `<div class="text-xs text-gray-500 mt-1">📎 來源：</div>`;
      msg.sources.forEach(s => {
        html += `<a href="${s.url}" target="_blank" class="block text-xs text-indigo-400 hover:text-indigo-300 truncate">${escHtml(s.title)}</a>`;
      });
    }
    html += `</div></details>`;
  }

  return html;
}

function setToolIndicator(text, color) {
  const colors = { yellow: 'bg-yellow-400', green: 'bg-emerald-400', red: 'bg-red-400', gray: 'bg-gray-500' };
  toolIndicator.innerHTML = `<span class="w-1.5 h-1.5 rounded-full ${colors[color] || colors.gray}"></span> ${text}`;
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

function renderAndScroll() {
  renderMessages();
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// ── Optimize button ──────────────────────────────────────────────────────────
optimizeBtn.addEventListener('click', async () => {
  const lastAssistant = [...conversation].reverse().find(m => m.role === 'assistant' && !m.loading);
  if (!lastAssistant) return;
  conversation.push({ role: 'user', content: '請對你的上一個回答進行全局優化：完整性、效能、格式、安全、進化建議' });
  renderAndScroll();

  const optimizeMsg = { role: 'assistant', content: '', loading: true };
  conversation.push(optimizeMsg);
  renderAndScroll();

  try {
    const resp = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: '請優化上一個回答：完整性、效能、格式、安全、進化',
        search_enabled: searchToggle.checked,
        file_read_enabled: fileReadToggle.checked,
        history: conversation.filter(m => !m.loading)
      })
    });
    const data = await resp.json();
    optimizeMsg.content = data.reply || '（無回應）';
    optimizeMsg.loading = false;
  } catch {
    optimizeMsg.content = '⚠️ 優化請求失敗';
    optimizeMsg.loading = false;
  }
  renderAndScroll();
});
