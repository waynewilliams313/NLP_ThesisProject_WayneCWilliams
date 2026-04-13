CREATE TABLE IF NOT EXISTS progress (
    selected_order INTEGER PRIMARY KEY,
    word_id INTEGER NOT NULL UNIQUE,
    target_word TEXT NOT NULL,
    reading_correct INTEGER DEFAULT 0,
    writing_correct INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    attempts_reading INTEGER DEFAULT 0,
    attempts_writing INTEGER DEFAULT 0,
    last_reading_input TEXT,
    last_writing_input TEXT,
    updated_at TEXT
);
