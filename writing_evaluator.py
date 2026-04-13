from __future__ import annotations

from .dataset_loader import DatasetBundle
from .feedback_parser import WritingFeedback, parse_writing_feedback
from .input_normalizer import normalize_user_input
from .model_loader import ModelRuntime
from .progress_db import ProgressDB
from .prompt_builder import build_writing_prompt


def _mock_writing_feedback(item: dict, student_sentence: str) -> str:
    word = item["target_word"]
    pinyin = item["target_pinyin"]
    english = item["target_english"]
    is_correct = bool(student_sentence.strip())

    chinese = f"我{word}中文。" if word != "我" else "我是学生。"
    chinese = chinese if is_correct else f"请再试一次，使用“{word}”。"
    result = "Correct" if is_correct else "Incorrect"
    explanation = (
        "The sentence is acceptable for a beginner prototype response."
        if is_correct
        else f"Try writing a sentence that includes the target word '{word}'."
    )

    return (
        f"EVALUATION: {result}\n"
        f"CHINESE: {chinese}\n"
        f"PINYIN: {pinyin}\n"
        f"ENGLISH: {english}\n"
        f"IMPROVED_CHINESE: {chinese}\n"
        f"IMPROVED_PINYIN: {pinyin}\n"
        f"IMPROVED_ENGLISH: {english}\n"
        f"EXPLANATION: {explanation}"
    )


def evaluate_writing_sentence(
    dataset: DatasetBundle,
    runtime: ModelRuntime,
    word_id: int,
    student_sentence: str,
    progress_db: ProgressDB,
) -> WritingFeedback:
    item = dataset.writing_by_word_id[word_id]
    normalized = normalize_user_input(student_sentence)

    if runtime.use_mock:
        raw = _mock_writing_feedback(item, normalized.normalized_text)
    else:
        prompt = build_writing_prompt(item=item, student_sentence=normalized.normalized_text)
        raw = runtime.generate(prompt)

    feedback = parse_writing_feedback(raw)
    progress_db.mark_writing_attempt(
        word_id=word_id,
        user_input=normalized.normalized_text,
        correct=feedback.evaluation.lower() == "correct",
    )
    return feedback
