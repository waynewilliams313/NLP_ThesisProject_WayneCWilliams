from __future__ import annotations

from .dataset_loader import DatasetBundle, WordRecord
from .progress_db import ProgressDB


def get_current_word_record(dataset: DatasetBundle, progress_db: ProgressDB) -> WordRecord:
    word_id = progress_db.get_first_incomplete_word_id()
    for record in dataset.words:
        if record.word_id == word_id:
            return record
    raise KeyError(f"Word ID {word_id} not found in dataset.")


def mark_word_complete_and_advance(progress_db: ProgressDB, current_word_id: int) -> None:
    progress_db.mark_completed(current_word_id)


def repeat_current_word(progress_db: ProgressDB, current_word_id: int) -> None:
    progress_db.reset_word(current_word_id)
