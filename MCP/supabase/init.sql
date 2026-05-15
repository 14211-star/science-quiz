-- =============================================================
-- Supabase Schema for DeepSeek Bridge
-- Run this in Supabase SQL Editor
-- =============================================================

-- 1. Chat History
CREATE TABLE IF NOT EXISTS chat_history (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID DEFAULT gen_random_uuid(),
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  sources JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_chat_history_session ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created ON chat_history(created_at DESC);

-- 2. Search Log
CREATE TABLE IF NOT EXISTS search_log (
  id BIGSERIAL PRIMARY KEY,
  query TEXT NOT NULL,
  results JSONB DEFAULT '[]',
  result_count INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_search_log_query ON search_log USING gin(to_tsvector('simple', query));
CREATE INDEX IF NOT EXISTS idx_search_log_created ON search_log(created_at DESC);

-- 3. File Cache
CREATE TABLE IF NOT EXISTS file_cache (
  id BIGSERIAL PRIMARY KEY,
  file_path TEXT UNIQUE NOT NULL,
  content_hash TEXT NOT NULL,
  content TEXT NOT NULL,
  file_size INT DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_file_cache_path ON file_cache(file_path);

-- 4. Enable Row Level Security (optional)
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE search_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_cache ENABLE ROW LEVEL SECURITY;

-- 5. Anonymous access policies (adjust as needed)
CREATE POLICY "anon_select_chat" ON chat_history FOR SELECT USING (true);
CREATE POLICY "anon_insert_chat" ON chat_history FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_select_search" ON search_log FOR SELECT USING (true);
CREATE POLICY "anon_insert_search" ON search_log FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_select_file" ON file_cache FOR SELECT USING (true);
CREATE POLICY "anon_insert_file" ON file_cache FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_file" ON file_cache FOR UPDATE USING (true);
