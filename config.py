from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

APP_TITLE = "AI-Assisted Chinese Reading and Writing Tutor"
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")
USE_MOCK_MODEL = os.getenv("USE_MOCK_MODEL", "true").lower() == "true"
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "256"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

WORDS_CSV = DATA_DIR / "thesis_30_words_ready.csv"
READING_JSON = DATA_DIR / "thesis_30_reading_items.json"
WRITING_JSON = DATA_DIR / "thesis_30_writing_items.json"
DB_PATH = DATA_DIR / "progress_runtime.db"
SEED_DB_PATH = DATA_DIR / "thesis_30_progress_seed.db"
PROGRESS_SQL = DATA_DIR / "thesis_30_progress_init.sql"