# 三年級科學 · 模擬測驗系統

一個純前端、免後端的互動式測驗系統，適合小學三年級科學評量使用。

## 🌐 網址

**GitHub Pages：** https://14211-star.github.io/science-quiz/

**管理後台：** https://14211-star.github.io/science-quiz/admin.html

---

## 🔐 帳號與密碼

| 角色 | 進入方式 | 密碼 |
|------|----------|------|
| **學生** | 開啟網站 → 填入資料登入 | `2129` |
| **管理員** | 訪問 `/admin.html` | `admin123` |
| **查看答案** | 學生測驗時按「查看答案」按鈕 | `378` |

---

## 📚 功能總覽

### 學生測驗

- 選擇班級（甲～己）、輸入姓名、學號（1-40）、密碼登入
- 題目隨機排序
- 四種題型：**圖片選擇題**、**文字選擇題**、**簡答題**、**填充題**
- 36 分鐘倒數計時
- 答題狀態導航（灰＝未做、綠＝已做、藍＝目前）
- 儲存答案（按鈕閃爍回饋）
- 查看答案（需密碼）
- 匯出 XLSX（含批改，三 Sheet 格式）
- 電郵提交答案

### 管理後台（題庫管理）

- **題庫管理**：新增/編輯/刪除四種題型題目
- **出題設定**：自動出題（依題型設定數量隨機抽題）或手動選題
- **匯出 / 匯入 XLSX**：題庫可存成 Excel 檔編輯後再匯入
- **上傳到 GitHub**：匯入後可上傳到 GitHub，觸發 Actions 自動同步到網站
- **Cloudflare Worker**：題庫上傳透過 Cloudflare Worker 代理，無需輸入 GitHub Token

### 管理後台（考試結果）

- 匯入學生 XLSX 答案檔
- 自動合併全班成績
- 匯出全班總表（含正確率統計）

---

## 📋 XLSX 題庫格式

匯出的 `questions.xlsx` 包含以下欄位，可直接用 Excel 編輯：

| 欄位 | 說明 |
|------|------|
| ID | 題號 |
| 題型 | `image-choice` / `text-choice` / `short-answer` / `fill-blank` |
| 標題 | 題目標題 |
| 題目內容 | 題目文字（支援 HTML） |
| 選項A~D | 選擇題選項文字 |
| 正確答案 | 選擇題填正確選項字母，填充題填答案文字 |
| 多組答案 | 填充題多組答案用 `|` 分隔（如 `液態|液體`） |
| 圖片網址 | 圖片選擇題的圖片 URL |

編輯後存檔，可透過管理後台上傳到 GitHub 同步到網站。

---

## 🚀 部署方式

### GitHub Pages（推薦）

本系統已部署到 GitHub Pages，網址：https://14211-star.github.io/science-quiz/

**更新題庫流程：**

1. 在管理後台（`/admin.html`）匯入新的 `questions.xlsx`
2. 點擊「上傳到 GitHub」按鈕
3. 系統會自動透過 Cloudflare Worker 上傳到 GitHub
4. GitHub Actions 自動將 XLSX 轉換為 JSON，約 1-2 分鐘後題庫更新生效
5. 學生端會自動載入最新題庫

### 本機離線測試

```bash
# 在專案目錄開啟 HTTP 伺服器
python -m http.server 8080

# 開啟瀏覽器
http://localhost:8080
```

---

## 🛠 技術架構

- **純前端**：單一 HTML 檔案，無需後端伺服器
- **資料儲存**：題庫存在瀏覽器 `localStorage`
- **題庫同步**：Cloudflare Worker + GitHub Actions 自動將 `questions.xlsx` 轉換為 `questions.json`
- **Excel 處理**：使用 SheetJS 庫（前端）和 openpyxl（Actions）
- **樣式**：純 CSS，無框架依賴

### 檔案結構

```
science-quiz/
├── index.html              ← 學生測驗頁面（含內嵌管理後台）
├── admin.html              ← 獨立管理後台（XLSX 上傳同步）
├── questions.xlsx          ← 題庫來源檔案
├── questions.json          ← Actions 自動生成（學生端載入）
├── README.md               ← 說明文件
├── .github/
│   └── workflows/
│       ├── sync.yml        ← XLSX → JSON 轉換工作流
│       └── deploy.yml      ← 部署到 GitHub Pages 工作流
└── scripts/
    ├── parse_xlsx.py       ← XLSX 解析腳本（Actions 使用）
    └── generate_initial_xlsx.py  ← 生成初始題庫（一次性）
```

### GitHub Actions 工作流

| 工作流 | 觸發條件 | 功能 |
|--------|----------|------|
| **sync.yml** | `questions.xlsx` 變更 | 解析 XLSX → 生成 `questions.json` |
| **deploy.yml** | 程式碼推送 / sync 完成 | 部署所有檔案到 GitHub Pages |

---

## ⚠️ 注意事項

- 學生密碼和管理員密碼可透過瀏覽器開發工具修改，建議定期更換
- GitHub Token 已移至 Cloudflare Worker Secrets，前端不再暴露
- 清除瀏覽器資料會清除題庫和設定，請定期匯出備份
- GitHub Pages 更新約需 1-2 分鐘（Actions 執行時間）
- 管理員密碼為 `admin123`，任何電腦只需輸入此密碼即可上傳題庫

---

## ☁️ Cloudflare Worker 設定

題庫上傳功能依賴 Cloudflare Worker 代理 GitHub API 呼叫：

| 項目 | 說明 |
|------|------|
| **Worker URL** | `https://sparkling-night-1177.ab117395.workers.dev/upload` |
| **Secrets** | `GITHUB_TOKEN`, `GITHUB_REPO`, `ADMIN_PASSWORD` |
| **免費額度** | 10 萬次請求/天，絕對夠用 |

老師只需記住管理員密碼 `admin123`，即可在任何電腦上傳題庫，無需設定 GitHub Token。

---

## 📞 支援

如有問題，請前往 [GitHub Issues](https://github.com/14211-star/science-quiz/issues) 回報。
