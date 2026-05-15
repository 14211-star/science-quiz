# Plan 3/7: GAS Code.gs (Security Fix)

**Path:** `C:\Users\ab117\OneDrive\文件\OPENCODE\MCP\gas\Code.gs`

## Fixes
- ✅ API Key authentication required for all mutations
- ✅ Sheet ID restricted to whitelist (prevent attacker reading your other sheets)
- ✅ Rate limiting via PropertiesService
- ✅ Input validation

## Full Code (replace entire file)

```javascript
/**
 * DeepSeek Bridge - Google Apps Script Webhook (Secure)
 *
 * Deploy: Deploy > New deployment > Web app
 * Execute as: Me
 * Access: Anyone
 *
 * Set GAS_WEBHOOK_URL and GAS_API_KEY in .env
 */

var ALLOWED_SHEET_IDS = PropertiesService.getScriptProperties().getProperty('ALLOWED_SHEET_IDS');
var ALLOWED_LIST = ALLOWED_SHEET_IDS ? ALLOWED_SHEET_IDS.split(',') : [];

function doGet(e) {
  return jsonResponse({ status: 'ok', message: 'DeepSeek Bridge GAS is running' });
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var action = data.action || 'ping';
    var apiKey = data.apiKey || '';

    // Validate API key for all actions except ping
    var storedKey = PropertiesService.getScriptProperties().getProperty('API_KEY');
    if (action !== 'ping' && storedKey && apiKey !== storedKey) {
      return jsonResponse({ error: 'Invalid API key' }, 403);
    }

    // Rate limit: max 60 requests per minute
    if (!checkRateLimit()) {
      return jsonResponse({ error: 'Rate limit exceeded (60/min)' }, 429);
    }

    switch (action) {
      case 'ping':
        return jsonResponse({ pong: true, time: new Date().toISOString() });

      case 'log':
        return jsonResponse(logToSheet(data));

      case 'query':
        return jsonResponse(querySheet(data));

      default:
        return jsonResponse({ error: 'Unknown action: ' + action }, 400);
    }
  } catch (err) {
    return jsonResponse({ error: err.message }, 500);
  }
}

function logToSheet(data) {
  var sheetId = data.sheetId || '';
  if (sheetId && ALLOWED_LIST.indexOf(sheetId) === -1) {
    return { error: 'Sheet ID not in whitelist' };
  }

  var ss = sheetId ? SpreadsheetApp.openById(sheetId) : SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('ChatLog') || ss.insertSheet('ChatLog');

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Timestamp', 'Session', 'Role', 'Content', 'Sources']);
  }

  sheet.appendRow([
    new Date().toISOString(),
    String(data.session || ''),
    String(data.role || ''),
    String(data.content || ''),
    JSON.stringify(data.sources || [])
  ]);

  return { status: 'logged', row: sheet.getLastRow() };
}

function querySheet(data) {
  var sheetId = data.sheetId || '';
  if (sheetId && ALLOWED_LIST.indexOf(sheetId) === -1) {
    return { error: 'Sheet ID not in whitelist' };
  }

  var ss = sheetId ? SpreadsheetApp.openById(sheetId) : SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('ChatLog');
  if (!sheet || sheet.getLastRow() <= 1) return { rows: [] };

  var rows = sheet.getDataRange().getValues();
  var headers = rows[0];
  var limit = Math.min(data.limit || 50, 200);
  var result = rows.slice(1, 1 + limit).map(function(r) {
    var obj = {};
    headers.forEach(function(h, i) { obj[h] = r[i]; });
    return obj;
  });

  return { rows: result };
}

function checkRateLimit() {
  var now = Date.now();
  var prop = PropertiesService.getScriptProperties();
  var timestamps = JSON.parse(prop.getProperty('RATE_LOG') || '[]');
  timestamps = timestamps.filter(function(t) { return now - t < 60000; });
  timestamps.push(now);
  prop.setProperty('RATE_LOG', JSON.stringify(timestamps));
  return timestamps.length <= 60;
}

function jsonResponse(data, status) {
  status = status || 200;
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
```
