from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadingFeedback:
    result: str
    chinese: str
    pinyin: str
    english: str
    explanation: str

    def to_markdown(self) -> str:
        return (
            f"### Reading Feedback\n"
            f"**Result:** {self.result}\n\n"
            f"**Chinese:** {self.chinese}\n\n"
            f"**Pinyin:** {self.pinyin}\n\n"
            f"**English:** {self.english}\n\n"
            f"**Explanation:** {self.explanation}"
        )


@dataclass(frozen=True)
class WritingFeedback:
    evaluation: str
    chinese: str
    pinyin: str
    english: str
    improved_chinese: str
    improved_pinyin: str
    improved_english: str
    explanation: str

    def to_markdown(self) -> str:
        return (
            f"### Writing Feedback\n"
            f"**Evaluation:** {self.evaluation}\n\n"
            f"**Chinese:** {self.chinese}\n\n"
            f"**Pinyin:** {self.pinyin}\n\n"
            f"**English:** {self.english}\n\n"
            f"**Improved Chinese:** {self.improved_chinese}\n\n"
            f"**Improved Pinyin:** {self.improved_pinyin}\n\n"
            f"**Improved English:** {self.improved_english}\n\n"
            f"**Explanation:** {self.explanation}"
        )


def _parse_lines(raw_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in raw_text.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().upper()] = value.strip()
    return fields


def parse_reading_feedback(raw_text: str) -> ReadingFeedback:
    fields = _parse_lines(raw_text)
    required = ["RESULT", "CHINESE", "PINYIN", "ENGLISH", "EXPLANATION"]
    missing = [key for key in required if key not in fields or not fields[key]]
    if missing:
        raise ValueError(f"Missing reading feedback fields: {missing}")
    return ReadingFeedback(
        result=fields["RESULT"],
        chinese=fields["CHINESE"],
        pinyin=fields["PINYIN"],
        english=fields["ENGLISH"],
        explanation=fields["EXPLANATION"],
    )


def parse_writing_feedback(raw_text: str) -> WritingFeedback:
    fields = _parse_lines(raw_text)
    required = [
        "EVALUATION",
        "CHINESE",
        "PINYIN",
        "ENGLISH",
        "IMPROVED_CHINESE",
        "IMPROVED_PINYIN",
        "IMPROVED_ENGLISH",
        "EXPLANATION",
    ]
    missing = [key for key in required if key not in fields or not fields[key]]
    if missing:
        raise ValueError(f"Missing writing feedback fields: {missing}")
    return WritingFeedback(
        evaluation=fields["EVALUATION"],
        chinese=fields["CHINESE"],
        pinyin=fields["PINYIN"],
        english=fields["ENGLISH"],
        improved_chinese=fields["IMPROVED_CHINESE"],
        improved_pinyin=fields["IMPROVED_PINYIN"],
        improved_english=fields["IMPROVED_ENGLISH"],
        explanation=fields["EXPLANATION"],
    )
