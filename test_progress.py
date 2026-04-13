from pathlib import Path
import shutil

from src.progress_db import ProgressDB
from src.config import SEED_DB_PATH


def test_progress_db_summary(tmp_path):
    db_path = tmp_path / "progress_test.db"
    shutil.copy2(SEED_DB_PATH, db_path)
    db = ProgressDB(db_path=db_path)
    summary = db.get_progress_summary()
    assert summary["total_words"] == 50
    assert summary["completed_words"] == 0
