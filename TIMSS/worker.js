// Cloudflare Worker — 題庫 XLSX 上傳到 GitHub
// 部署方式：
// 1. 到 cloudflare.com → Workers & Pages → 建立 Worker
// 2. 貼上此程式碼 → 儲存並部署
// 3. 到 Worker 設定 → 變數 → 新增以下 Secrets：
//    GITHUB_TOKEN = 你的 GitHub Personal Access Token
//    GITHUB_REPO = 14211-star/science-quiz
// 4. 將產生的 Worker URL 填入 HTML 中的 WORKER_URL

export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const token = env.GITHUB_TOKEN;
    const repo = env.GITHUB_REPO;
    if (!token || !repo) {
      return new Response(JSON.stringify({ error: 'Server not configured' }), {
        status: 500, headers: { 'Content-Type': 'application/json' }
      });
    }

    let body;
    try { body = await request.json(); } catch {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
        status: 400, headers: { 'Content-Type': 'application/json' }
      });
    }

    const xlsxBase64 = body.xlsx;
    if (!xlsxBase64) {
      return new Response(JSON.stringify({ error: 'Missing xlsx data' }), {
        status: 400, headers: { 'Content-Type': 'application/json' }
      });
    }

    const path = 'questions.xlsx';
    const url = `https://api.github.com/repos/${repo}/contents/${path}`;

    try {
      // Step 1: Get existing file SHA (if any)
      const getResp = await fetch(url, {
        headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github.v3+json' }
      });
      const existing = getResp.ok ? await getResp.json() : { sha: '' };
      const sha = existing.sha || '';

      // Step 2: Upload new file
      const putResp = await fetch(url, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: 'Update question bank via Worker upload',
          content: xlsxBase64,
          sha: sha || undefined
        })
      });

      if (!putResp.ok) {
        const errData = await putResp.text();
        return new Response(JSON.stringify({ error: `GitHub API error: ${putResp.status}`, detail: errData }), {
          status: 502, headers: { 'Content-Type': 'application/json' }
        });
      }

      return new Response(JSON.stringify({ ok: true }), {
        status: 200, headers: { 'Content-Type': 'application/json' }
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500, headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};
