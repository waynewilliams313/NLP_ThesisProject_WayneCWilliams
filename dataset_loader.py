from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import READING_JSON, WORDS_CSV, WRITING_JSON


@dataclass(frozen=True)
class WordRecord:
    selected_order: int
    word_id: int
    word: str
    pinyin: str
    english: str
    category: str


@dataclass(frozen=True)
class DatasetBundle:
    words: list[WordRecord]
    reading_by_word_id: dict[int, dict[str, Any]]
    writing_by_word_id: dict[int, dict[str, Any]]


def _load_words(csv_path: Path) -> list[WordRecord]:
    rows: list[WordRecord] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                WordRecord(
                    selected_order=int(row["selected_order"]),
                    word_id=int(row["word_id"]),
                    word=row["word"].strip(),
                    pinyin=row["pinyin"].strip(),
                    english=row["english"].strip(),
                    category=row["category"].strip(),
                )
            )
    if not rows:
        raise ValueError("No words were loaded from the CSV dataset.")
    return rows


def _load_json_by_word_id(json_path: Path) -> dict[int, dict[str, Any]]:
    with json_path.open("r", encoding="utf-8") as f:
        items = json.load(f)
    if not isinstance(items, list) or not items:
        raise ValueError(f"Expected a non-empty list in {json_path}.")
    out: dict[int, dict[str, Any]] = {}
    for item in items:
        word_id = int(item["word_id"])
        out[word_id] = item
    return out


def load_dataset_bundle() -> DatasetBundle:
    words = _load_words(WORDS_CSV)
    reading = _load_json_by_word_id(READING_JSON)
    writing = _load_json_by_word_id(WRITING_JSON)

    word_ids = {w.word_id for w in words}
    if set(reading.keys()) != word_ids:
        missing = sorted(word_ids - set(reading.keys()))
        extra = sorted(set(reading.keys()) - word_ids)
        raise ValueError(f"Reading dataset mismatch. Missing={missing} Extra={extra}")
    if set(writing.keys()) != word_ids:
        missing = sorted(word_ids - set(writing.keys()))
        extra = sorted(set(writing.keys()) - word_ids)
        raise ValueError(f"Writing dataset mismatch. Missing={missing} Extra={extra}")

    return DatasetBundle(words=words, reading_by_word_id=reading, writing_by_word_id=writing)
