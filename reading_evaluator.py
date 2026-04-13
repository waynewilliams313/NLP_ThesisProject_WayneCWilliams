from __future__ import annotations

from .dataset_loader import DatasetBundle
from .feedback_parser import ReadingFeedback, parse_reading_feedback
from .input_normalizer import normalize_user_input, normalize_chinese, normalize_pinyin
from .model_loader import ModelRuntime
from .progress_db import ProgressDB
from .prompt_builder import build_reading_prompt


def _contains_chinese(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _extract_normalized_text(normalized_obj) -> str:
    """
    Supports either:
    - an object with .normalized_text
    - a tuple like (input_type, normalized_text)
    - a plain string
    """
    if hasattr(normalized_obj, "normalized_text"):
        return normalized_obj.normalized_text

    if isinstance(normalized_obj, tuple) and len(normalized_obj) == 2:
        return normalized_obj[1]

    return str(normalized_obj)


def is_reading_answer_correct(
    user_answer: str,
    expected_zh: str,
    expected_pinyin: str,
    expected_english: str = "",
) -> bool:
    raw = (user_answer or "").strip()
    if not raw:
        return False

    # Chinese input
    if _contains_chinese(raw):
        return normalize_chinese(raw) == normalize_chinese(expected_zh)

    # Pinyin input (tone marks or no tone marks)
    if normalize_pinyin(raw) == normalize_pinyin(expected_pinyin):
        return True

    # Optional English support
    if expected_english and raw.lower().strip() == expected_english.lower().strip():
        return True

    return False


def _mock_reading_feedback(item: dict, student_answer: str) -> str:
    is_correct = is_reading_answer_correct(
        user_answer=student_answer,
        expected_zh=item["answer_chinese"],
        expected_pinyin=item["answer_pinyin"],
        expected_english=item["answer_english"],
    )

    result = "Correct" if is_correct else "Incorrect"
    explanation = (
        f"Correct. The passage supports the answer '{item['answer_chinese']}'."
        if is_correct
        else f"Incorrect. The correct answer is '{item['answer_chinese']}'."
    )

    return (
        f"RESULT: {result}\n"
        f"CHINESE: {item['answer_chinese']}\n"
        f"PINYIN: {item['answer_pinyin']}\n"
        f"ENGLISH: {item['answer_english']}\n"
        f"EXPLANATION: {explanation}"
    )


def evaluate_reading_answer(
    dataset: DatasetBundle,
    runtime: ModelRuntime,
    word_id: int,
    student_answer: str,
    progress_db: ProgressDB,
) -> ReadingFeedback:
    item = dataset.reading_by_word_id[word_id]
    normalized_obj = normalize_user_input(student_answer)
    normalized_text = _extract_normalized_text(normalized_obj)

    if runtime.use_mock:
        raw = _mock_reading_feedback(item, student_answer)
    else:
        prompt = build_reading_prompt(item=item, student_answer=normalized_text)
        raw = runtime.generate(prompt)

    feedback = parse_reading_feedback(raw)
    progress_db.mark_reading_attempt(
        word_id=word_id,
        user_input=normalized_text,
        correct=feedback.result.lower() == "correct",
    )
    return feedback
