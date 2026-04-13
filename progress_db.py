from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

from .config import DB_PATH, SEED_DB_PATH


class ProgressDB:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or DB_PATH
        if not self.db_path.exists():
            shutil.copy2(SEED_DB_PATH, self.db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_progress_summary(self) -> dict[str, int]:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) AS c FROM progress").fetchone()["c"]
            completed = conn.execute("SELECT COUNT(*) AS c FROM progress WHERE completed = 1").fetchone()["c"]
        return {"total_words": total, "completed_words": completed}

    def get_first_incomplete_word_id(self) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT word_id FROM progress WHERE completed = 0 ORDER BY selected_order ASC LIMIT 1"
            ).fetchone()
            if row is None:
                row = conn.execute("SELECT word_id FROM progress ORDER BY selected_order ASC LIMIT 1").fetchone()
            return int(row["word_id"])

    def mark_reading_attempt(self, word_id: int, user_input: str, correct: bool) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE progress
                SET attempts_reading = attempts_reading + 1,
                    last_reading_input = ?,
                    reading_correct = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE word_id = ?
                """,
                (user_input, 1 if correct else 0, word_id),
            )
            conn.commit()

    def mark_writing_attempt(self, word_id: int, user_input: str, correct: bool) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE progress
                SET attempts_writing = attempts_writing + 1,
                    last_writing_input = ?,
                    writing_correct = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE word_id = ?
                """,
                (user_input, 1 if correct else 0, word_id),
            )
            conn.commit()

    def mark_completed(self, word_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE progress SET completed = 1, updated_at = CURRENT_TIMESTAMP WHERE word_id = ?",
                (word_id,),
            )
            conn.commit()

    def reset_word(self, word_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE progress
                SET reading_correct = 0,
                    writing_correct = 0,
                    completed = 0,
                    attempts_reading = 0,
                    attempts_writing = 0,
                    last_reading_input = NULL,
                    last_writing_input = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE word_id = ?
                """,
                (word_id,),
            )
            conn.commit()

    def get_word_status(self, word_id: int) -> dict:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM progress WHERE word_id = ?", (word_id,)).fetchone()
            if row is None:
                raise KeyError(f"Unknown word_id: {word_id}")
            return dict(row)
