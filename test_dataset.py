from src.dataset_loader import load_dataset_bundle


def test_load_dataset_bundle():
    bundle = load_dataset_bundle()
    assert len(bundle.words) == 50
    assert len(bundle.reading_by_word_id) == 50
    assert len(bundle.writing_by_word_id) == 50
