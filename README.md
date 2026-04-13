# AI-Assisted Chinese Reading and Writing Tutor (HSK 3.0 Band 1 Prototype)

This project is a thesis-ready starter implementation for an AI-assisted Chinese learning app built around a **word-centered loop**:

1. Select a target word from a 50-word thesis subset
2. Show a scaffolded reading passage (Chinese + Pinyin + English)
3. Check a comprehension answer
4. Show a writing prompt using the same target word
5. Evaluate the learner's sentence
6. Save progress and move to the next word

## Data sources included
- `data/thesis_50_words_ready.csv`
- `data/reading_items.json`
- `data/writing_items.json`
- `data/progress_init.sql`
- `data/progress_seed.db`
- `data/Official_vocabulary_band1.pdf`

## Important implementation note
The **official Band 1 PDF** is the source of truth for the official vocabulary list. The reading passages, questions, and writing prompts are prototype lesson content created for this thesis system.

## Quick start

### 1. Create a virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
```

### 2. Run in mock mode first
Mock mode lets you test the full app structure without loading a large model.

```bash
set USE_MOCK_MODEL=true      # Windows PowerShell
# export USE_MOCK_MODEL=true # macOS/Linux
python app.py
```

### 3. Run with Qwen later
```bash
set USE_MOCK_MODEL=false      # Windows PowerShell
# export USE_MOCK_MODEL=false # macOS/Linux
python app.py
```

The app uses `Qwen/Qwen2.5-0.5B-Instruct` when mock mode is off.

## Recommended build order
1. Verify one word from start to finish in mock mode
2. Verify the same word with the real Qwen model
3. Test 10 words
4. Test all 50 thesis words
5. Add evaluation logs and screenshots for the thesis

## Files you will likely edit most
- `src/config.py`
- `src/reading_evaluator.py`
- `src/writing_evaluator.py`
- `src/feedback_parser.py`
- `app.py`

## Thesis-safe claim
The app architecture is designed to scale to the full official Band 1 curriculum, while this implementation and evaluation use a representative 50-word subset.
