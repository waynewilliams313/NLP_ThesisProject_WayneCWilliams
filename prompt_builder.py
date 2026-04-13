from __future__ import annotations


def build_reading_prompt(item: dict, student_answer: str) -> str:
    return f"""You are a beginner Chinese tutor.

Evaluate the student's answer to the reading question.

Target word:
Chinese: {item['target_word']}
Pinyin: {item['target_pinyin']}
English: {item['target_english']}

Passage:
Chinese: {item['passage_chinese']}
Pinyin: {item['passage_pinyin']}
English: {item['passage_english']}

Question:
Chinese: {item['question_chinese']}
Pinyin: {item['question_pinyin']}
English: {item['question_english']}

Correct answer:
Chinese: {item['answer_chinese']}
Pinyin: {item['answer_pinyin']}
English: {item['answer_english']}

Student answer: {student_answer}

Return exactly in this format:
RESULT: <Correct or Incorrect>
CHINESE: <correct answer in Chinese>
PINYIN: <correct answer in tone-marked pinyin>
ENGLISH: <correct answer in English>
EXPLANATION: <short beginner-friendly explanation>
"""


def build_writing_prompt(item: dict, student_sentence: str) -> str:
    return f"""You are a beginner Chinese tutor.

Evaluate the student's sentence.

Target word:
Chinese: {item['target_word']}
Pinyin: {item['target_pinyin']}
English: {item['target_english']}

Prompt:
Chinese: {item['prompt_chinese']}
Pinyin: {item['prompt_pinyin']}
English: {item['prompt_english']}

Student sentence: {student_sentence}

Return exactly in this format:
EVALUATION: <Correct or Incorrect>
CHINESE: <best Chinese version>
PINYIN: <tone-marked pinyin>
ENGLISH: <English translation>
IMPROVED_CHINESE: <one improved sentence>
IMPROVED_PINYIN: <improved tone-marked pinyin>
IMPROVED_ENGLISH: <improved English translation>
EXPLANATION: <short beginner-friendly explanation>
"""
