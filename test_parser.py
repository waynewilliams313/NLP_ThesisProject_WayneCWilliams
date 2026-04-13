from src.feedback_parser import parse_reading_feedback, parse_writing_feedback


def test_parse_reading_feedback_ok():
    raw = """RESULT: Correct
CHINESE: 他学习中文。
PINYIN: Tā xuéxí Zhōngwén.
ENGLISH: He studies Chinese.
EXPLANATION: Correct answer.
"""
    parsed = parse_reading_feedback(raw)
    assert parsed.result == "Correct"
    assert parsed.chinese == "他学习中文。"


def test_parse_writing_feedback_ok():
    raw = """EVALUATION: Correct
CHINESE: 我学习中文。
PINYIN: Wǒ xuéxí Zhōngwén.
ENGLISH: I study Chinese.
IMPROVED_CHINESE: 我每天学习中文。
IMPROVED_PINYIN: Wǒ měitiān xuéxí Zhōngwén.
IMPROVED_ENGLISH: I study Chinese every day.
EXPLANATION: Good sentence.
"""
    parsed = parse_writing_feedback(raw)
    assert parsed.evaluation == "Correct"
    assert parsed.improved_chinese == "我每天学习中文。"
