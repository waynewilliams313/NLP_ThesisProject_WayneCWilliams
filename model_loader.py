from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .config import MAX_NEW_TOKENS, MODEL_NAME, TEMPERATURE, USE_MOCK_MODEL


@dataclass
class ModelRuntime:
    use_mock: bool
    model_name: str
    tokenizer: Optional[object] = None
    model: Optional[object] = None

    def generate(self, prompt: str) -> str:
        if self.use_mock:
            raise RuntimeError("Mock runtime does not use free-form generation.")
        if self.tokenizer is None or self.model is None:
            raise RuntimeError("Model runtime is not loaded.")

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            do_sample=False,
        )
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text[len(prompt):].strip() if text.startswith(prompt) else text.strip()


def build_model_runtime() -> ModelRuntime:
    if USE_MOCK_MODEL:
        return ModelRuntime(use_mock=True, model_name=MODEL_NAME)

    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )
    return ModelRuntime(use_mock=False, model_name=MODEL_NAME, tokenizer=tokenizer, model=model)
