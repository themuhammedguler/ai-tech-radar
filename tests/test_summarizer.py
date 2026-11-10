"""
Unit tests for text summarization.
Verifies sentence boundary detection, length bounds, and abbreviation handling.
"""

from src.processors.text_summarizer import extract_smart_summary


def test_handles_empty_input():
    assert extract_smart_summary("") == "Özet bulunamadı."
    assert extract_smart_summary("   ") == "Özet bulunamadı."


def test_extracts_clean_sentences():
    text = (
        "Large language models have achieved impressive reasoning. "
        "However, they struggle with spatial reasoning tasks. "
        "We introduce a novel dataset to benchmark 3D abilities."
    )
    summary = extract_smart_summary(text, max_chars=150)
    # Should include first two sentences cleanly
    assert "Large language models have achieved impressive reasoning." in summary
    assert "However, they struggle with spatial reasoning tasks." in summary
    assert summary.endswith(".")


def test_handles_abbreviations_without_false_splits():
    text = (
        "We evaluate models on difficult benchmarks, e.g., GSM8k and MATH. "
        "Our method achieves state-of-the-art results across all tasks."
    )
    summary = extract_smart_summary(text, max_chars=300)
    assert "e.g., GSM8k and MATH." in summary
    assert "Our method achieves state-of-the-art" in summary


def test_escapes_markdown_pipe_characters():
    text = "Model A | Model B comparison. Results show 99% accuracy."
    summary = extract_smart_summary(text)
    assert "|" not in summary
    assert "-" in summary
