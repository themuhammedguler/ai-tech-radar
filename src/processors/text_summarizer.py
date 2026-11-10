"""
Text summarization processor.
Extracts complete, coherent sentences from academic paper abstracts,
preventing awkward mid-word and mid-sentence truncations.
"""

import re
from src.config import SUMMARY_MAX_CHARS, SUMMARY_MIN_CHARS


def extract_smart_summary(
    raw_summary: str,
    max_chars: int = SUMMARY_MAX_CHARS,
    min_chars: int = SUMMARY_MIN_CHARS
) -> str:
    """
    Extracts 1 to 3 complete sentences from a text summary while respecting length bounds.

    Args:
        raw_summary: The raw abstract/summary string.
        max_chars: Maximum preferred character budget.
        min_chars: Minimum character threshold before stopping sentence collection.

    Returns:
        A cleanly formatted, complete-sentence summary string.
    """
    if not raw_summary or not raw_summary.strip():
        return "Özet bulunamadı."

    # Normalize whitespace and escape markdown table delimiters
    cleaned_text = re.sub(r"\s+", " ", raw_summary).strip()
    cleaned_text = cleaned_text.replace("|", "-")

    # Split on sentence terminals followed by space, taking care of common abbreviations
    # Negative lookbehind for common abbreviations like e.g., i.e., et al., Fig., vs.
    sentence_split_regex = r"(?<!\be\.g)(?<!\bi\.e)(?<!\bet al)(?<!\bFig)(?<!\bvs)(?<=[.!?])\s+"
    raw_sentences = re.split(sentence_split_regex, cleaned_text)

    selected_sentences: list[str] = []
    current_length = 0

    for sentence in raw_sentences:
        s_clean = sentence.strip()
        if not s_clean:
            continue

        sentence_len = len(s_clean)
        # Always pick at least the first sentence
        if not selected_sentences:
            selected_sentences.append(s_clean)
            current_length += sentence_len
        elif (current_length + 1 + sentence_len) <= max_chars:
            selected_sentences.append(s_clean)
            current_length += 1 + sentence_len
        elif current_length < min_chars:
            # If current length is too short, include next sentence if reasonable
            selected_sentences.append(s_clean)
            current_length += 1 + sentence_len
            break
        else:
            break

    result = " ".join(selected_sentences).strip()

    # If the first sentence alone exceeded max_chars significantly, gracefully truncate at word boundary
    if len(result) > (max_chars + 50):
        truncated = result[:max_chars].rsplit(" ", 1)[0].rstrip(" ,;:-")
        result = f"{truncated}..."

    return result
