from __future__ import annotations

import re
import unicodedata


def has_chinese(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def normalize_chinese(text: str) -> str:
    text = text.strip()
    text = text.replace("，", "")
    text = text.replace("。", "")
    text = text.replace("？", "")
    text = text.replace("！", "")
    text = text.replace("：", "")
    text = text.replace("；", "")
    text = text.replace(",", "")
    text = text.replace(".", "")
    text = text.replace("?", "")
    text = text.replace("!", "")
    text = text.replace(":", "")
    text = text.replace(";", "")
    text = re.sub(r"\s+", "", text)
    return text


def strip_pinyin_tones(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = unicodedata.normalize("NFC", text)
    return text


def normalize_pinyin(text: str) -> str:
    text = text.strip().lower()

    # optional handling for common keyboard input variants
    text = text.replace("ü", "u")
    text = text.replace("u:", "u")
    text = text.replace("v", "u")

    text = strip_pinyin_tones(text)

    # remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # collapse spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_user_input(text: str) -> tuple[str, str]:
    if has_chinese(text):
        return "zh", normalize_chinese(text)
    return "pinyin", normalize_pinyin(text)