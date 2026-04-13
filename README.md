# NLP Thesis Project – Wayne C. Williams

> This repository contains the source code, tests, configuration, and processed project data files for my NLP thesis project. It is organized for academic review of the project’s design, implementation, and evaluation framework.

## Project Overview

This repository supports a thesis project in **Natural Language Processing (NLP)** focused on **beginner-level Chinese reading and writing assistance**. The project explores how a Qwen-based language model can be used within an application that supports structured vocabulary-constrained tasks, reading evaluation, writing evaluation, feedback generation, and learner progress tracking.

The system is designed around **HSK Band 1 and Band 2 vocabulary** and is intended to investigate whether a fine-tuned model performs better than a non-fine-tuned baseline under the same controlled task setting.

## Research Objective

The main objective of this thesis project is to evaluate whether **fine-tuning Qwen on HSK Band 1 and Band 2 vocabulary-based data** improves performance for beginner-level Chinese reading and writing tasks when compared with a **baseline Qwen model without fine-tuning**, using the same vocabulary constraints.

More specifically, the project examines whether fine-tuning leads to stronger task performance, more appropriate vocabulary usage, and better support for controlled beginner-level Chinese language learning activities.

## Model Conditions

The project is designed around two main model conditions:

- **Baseline model:** Qwen used **without fine-tuning**, with tasks constrained to **HSK Band 1 and Band 2 vocabulary**
- **Fine-tuned model:** Qwen **fine-tuned** for the same **HSK Band 1 and Band 2 vocabulary-based task setting**

These two conditions are intended to be evaluated within the same application framework so that differences in performance can be measured under comparable conditions.

## Evaluation Design

The baseline and fine-tuned Qwen models are intended to be **evaluated and compared using cross-validation** to measure differences in performance.

The evaluation design is structured to support comparison between the two model conditions under the same beginner-level vocabulary constraints. The goal is to determine whether fine-tuning improves the quality and consistency of outputs for reading- and writing-related tasks in the application.

Depending on the final experimental setup described in the thesis document, evaluation may include performance measures relevant to NLP task quality, response appropriateness, and controlled vocabulary usage.

## System Purpose

This application is designed as an **AI-assisted Chinese reading and writing tutor** for beginner-level use. It supports structured educational interactions while remaining grounded in an NLP-focused system design.

The repository demonstrates:

- application implementation
- modular NLP-related project components
- dataset loading and processing
- reading and writing evaluation workflows
- feedback parsing and prompt construction
- learner progress tracking
- supporting test files
- processed dataset and initialization files used by the project

## Repository Structure

### Root Files

- `app.py` – main application entry point
- `README.md` – repository overview, academic context, and usage notes
- `requirements.txt` – Python dependencies required for the project

### Source Code Modules

The `src` portion of the project contains the main application and processing logic, including:

- `config.py` – configuration settings and project file paths
- `dataset_loader.py` – loads project dataset files
- `feedback_parser.py` – parses and structures feedback responses
- `input_normalizer.py` – normalizes and preprocesses user input
- `model_loader.py` – handles model-related loading logic
- `progress_db.py` – manages learner progress database operations
- `prompt_builder.py` – constructs prompts for the application workflow
- `reading_evaluator.py` – supports reading-related evaluation logic
- `ui_helpers.py` – helper functions for interface-related tasks
- `word_selector.py` – selects vocabulary items for activities
- `writing_evaluator.py` – supports writing-related evaluation logic

### Test Files

The repository includes test files for selected components:

- `test_dataset.py`
- `test_parser.py`
- `test_progress.py`

These tests help verify core functionality of the dataset, parsing, and progress-related modules.

### Data Files

The public repository includes processed project files used by the application, such as:

- `thesis_30_progress_init.sql`
- `thesis_30_reading_items.json`
- `thesis_30_words_checked.csv`
- `thesis_30_words_ready.csv`
- `thesis_30_writing_items.json`

These files support structured reading and writing tasks, vocabulary organization, and project database initialization.

## Application Workflow

At a high level, the system is intended to support the following workflow:

1. Load processed vocabulary and task-related data files
2. Select or prepare structured beginner-level reading or writing items
3. Accept and normalize user input
4. Build prompts and route processing through the application pipeline
5. Evaluate reading or writing responses
6. Parse and structure feedback
7. Record and update learner progress for later analysis

This workflow allows the project to function not only as an application prototype, but also as an evaluable NLP system within the thesis context.

## Dataset and Vocabulary Scope

This project is intentionally constrained to **HSK Band 1 and Band 2 vocabulary** in order to maintain a controlled beginner-level task environment.

The purpose of this vocabulary restriction is to:

- reduce task complexity
- align the system with beginner-level Chinese learning needs
- support clearer baseline-versus-fine-tuned model comparison
- provide a more structured evaluation setting for thesis analysis

The public repository includes **processed project data files** used by the system. Some source or reference materials used during dataset preparation are not redistributed in this public version of the repository.

## Public Repository Note

This GitHub repository is a **public academic project version** prepared for review of the project structure, codebase, and evaluation framework.

For public-sharing and repository-cleanliness reasons:

- temporary runtime files are excluded
- local virtual environment files are excluded
- cache files are excluded
- old unused files are excluded
- certain raw source/reference materials are not redistributed in this repository

This repository therefore emphasizes the implementation and processed project resources appropriate for public academic review.

## Setup and Execution

To run the project locally:

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
