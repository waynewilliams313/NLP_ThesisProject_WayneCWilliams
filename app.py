from __future__ import annotations

import gradio as gr

from src.config import APP_TITLE
from src.dataset_loader import DatasetBundle, load_dataset_bundle
from src.model_loader import build_model_runtime
from src.progress_db import ProgressDB
from src.reading_evaluator import evaluate_reading_answer
from src.writing_evaluator import evaluate_writing_sentence
from src.word_selector import get_current_word_record, mark_word_complete_and_advance, repeat_current_word


def build_app() -> gr.Blocks:
    dataset: DatasetBundle = load_dataset_bundle()
    runtime = build_model_runtime()
    progress_db = ProgressDB()

    def load_current_state():
        current = get_current_word_record(dataset, progress_db)
        reading = dataset.reading_by_word_id[current.word_id]
        writing = dataset.writing_by_word_id[current.word_id]
        progress = progress_db.get_progress_summary()

        return {
            "selected_order": current.selected_order,
            "word_id": current.word_id,
            "word": current.word,
            "pinyin": current.pinyin,
            "english": current.english,
            "category": current.category,
            "passage_chinese": reading["passage_chinese"],
            "passage_pinyin": reading["passage_pinyin"],
            "passage_english": reading["passage_english"],
            "question_chinese": reading["question_chinese"],
            "question_pinyin": reading["question_pinyin"],
            "question_english": reading["question_english"],
            "writing_prompt_chinese": writing["prompt_chinese"],
            "writing_prompt_pinyin": writing["prompt_pinyin"],
            "writing_prompt_english": writing["prompt_english"],
            "progress_text": (
                f"Progress: {progress['completed_words']} / {progress['total_words']} completed | "
                f"Current word: #{current.selected_order}"
            ),
        }

    def refresh_ui():
        state = load_current_state()
        return (
            state,
            state["progress_text"],
            state["word"],
            state["pinyin"],
            state["english"],
            state["category"],
            state["passage_chinese"],
            state["passage_pinyin"],
            state["passage_english"],
            state["question_chinese"],
            state["question_pinyin"],
            state["question_english"],
            state["writing_prompt_chinese"],
            state["writing_prompt_pinyin"],
            state["writing_prompt_english"],
            "",
            "",
        )

    def handle_reading_answer(student_answer: str, state: dict):
        result = evaluate_reading_answer(
            dataset=dataset,
            runtime=runtime,
            word_id=int(state["word_id"]),
            student_answer=student_answer,
            progress_db=progress_db,
        )
        return result.to_markdown()

    def handle_writing_answer(student_sentence: str, state: dict):
        result = evaluate_writing_sentence(
            dataset=dataset,
            runtime=runtime,
            word_id=int(state["word_id"]),
            student_sentence=student_sentence,
            progress_db=progress_db,
        )
        return result.to_markdown()

    def handle_next_word(state: dict):
        mark_word_complete_and_advance(progress_db=progress_db, current_word_id=int(state["word_id"]))
        return refresh_ui()

    def handle_repeat_word(state: dict):
        repeat_current_word(progress_db=progress_db, current_word_id=int(state["word_id"]))
        return refresh_ui()

    with gr.Blocks(title=APP_TITLE) as demo:
        gr.Markdown(f"# {APP_TITLE}")
        state = gr.State(value={})

        progress_text = gr.Markdown()

        with gr.Row():
            word = gr.Textbox(label="Target Word (Chinese)", interactive=False)
            pinyin = gr.Textbox(label="Pinyin", interactive=False)
            english = gr.Textbox(label="English", interactive=False)
            category = gr.Textbox(label="Category", interactive=False)

        with gr.Tabs():
            with gr.Tab("Reading Practice"):
                passage_chinese = gr.Textbox(label="Passage (Chinese)", lines=3, interactive=False)
                passage_pinyin = gr.Textbox(label="Passage (Pinyin)", lines=3, interactive=False)
                passage_english = gr.Textbox(label="Passage (English)", lines=3, interactive=False)
                question_chinese = gr.Textbox(label="Question (Chinese)", interactive=False)
                question_pinyin = gr.Textbox(label="Question (Pinyin)", interactive=False)
                question_english = gr.Textbox(label="Question (English)", interactive=False)
                reading_input = gr.Textbox(label="Your Answer (Chinese or Pinyin)", lines=2)
                reading_submit = gr.Button("Check Reading Answer")
                reading_feedback = gr.Markdown("")
                reading_answer = gr.Textbox(...)
                check_reading_btn = gr.Button(...)
                reading_feedback_text = (
                    f"**Grammar:** {feedback.grammar}\n\n"
                    f"**Alternative:** {feedback.alternative}"
)

            with gr.Tab("Writing Practice"):
                writing_prompt_chinese = gr.Textbox(label="Prompt (Chinese)", interactive=False)
                writing_prompt_pinyin = gr.Textbox(label="Prompt (Pinyin)", interactive=False)
                writing_prompt_english = gr.Textbox(label="Prompt (English)", interactive=False)
                writing_input = gr.Textbox(label="Your Sentence (Chinese or Pinyin)", lines=3)
                writing_submit = gr.Button("Check Writing")
                writing_feedback = gr.Markdown()


        with gr.Row():
            repeat_btn = gr.Button("Repeat Current Word")
            next_btn = gr.Button("Mark Complete and Next Word")

        demo.load(
            fn=refresh_ui,
            inputs=None,
            outputs=[
                state,
                progress_text,
                word,
                pinyin,
                english,
                category,
                passage_chinese,
                passage_pinyin,
                passage_english,
                question_chinese,
                question_pinyin,
                question_english,
                writing_prompt_chinese,
                writing_prompt_pinyin,
                writing_prompt_english,
                reading_input,
                writing_input,
            ],
        )

        reading_submit.click(
            fn=handle_reading_answer,
            inputs=[reading_input, state],
            outputs=[reading_feedback],
        )

        writing_submit.click(
            fn=handle_writing_answer,
            inputs=[writing_input, state],
            outputs=[writing_feedback],
        )

        repeat_btn.click(
            fn=handle_repeat_word,
            inputs=[state],
            outputs=[
                state,
                progress_text,
                word,
                pinyin,
                english,
                category,
                passage_chinese,
                passage_pinyin,
                passage_english,
                question_chinese,
                question_pinyin,
                question_english,
                writing_prompt_chinese,
                writing_prompt_pinyin,
                writing_prompt_english,
                reading_input,
                writing_input,
            ],
        )

        next_btn.click(
            fn=handle_next_word,
            inputs=[state],
            outputs=[
                state,
                progress_text,
                word,
                pinyin,
                english,
                category,
                passage_chinese,
                passage_pinyin,
                passage_english,
                question_chinese,
                question_pinyin,
                question_english,
                writing_prompt_chinese,
                writing_prompt_pinyin,
                writing_prompt_english,
                reading_input,
                writing_input,
            ],
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch()
